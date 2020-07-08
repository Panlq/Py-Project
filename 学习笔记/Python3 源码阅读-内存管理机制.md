## Python内存管理机制

## Python 内存管理分层架构

```c++
/* An object allocator for Python.

   Here is an introduction to the layers of the Python memory architecture,
   showing where the object allocator is actually used (layer +2), It is
   called for every object allocation and deallocation (PyObject_New/Del),
   unless the object-specific allocators implement a proprietary allocation
   scheme (ex.: ints use a simple free list). This is also the place where
   the cyclic garbage collector operates selectively on container objects.


    Object-specific allocators
    _____   ______   ______       ________
   [ int ] [ dict ] [ list ] ... [ string ]       Python core         |
+3 | <----- Object-specific memory -----> | <-- Non-object memory --> |
    _______________________________       |                           |
   [   Python's object allocator   ]      |                           |
+2 | ####### Object memory ####### | <------ Internal buffers ------> |
    ______________________________________________________________    |
   [          Python's raw memory allocator (PyMem_ API)          ]   |
+1 | <----- Python memory (under PyMem manager's control) ------> |   |
    __________________________________________________________________
   [    Underlying general-purpose allocator (ex: C library malloc)   ]
 0 | <------ Virtual memory allocated for the python process -------> |

   =========================================================================
    _______________________________________________________________________
   [                OS-specific Virtual Memory Manager (VMM)               ]
-1 | <--- Kernel dynamic storage allocation & management (page-based) ---> |
    __________________________________   __________________________________
   [                                  ] [                                  ]
-2 | <-- Physical memory: ROM/RAM --> | | <-- Secondary storage (swap) --> |

*/
```

reference：[Objects/obmalloc.c](https://github.com/python/cpython/blob/3.8/Objects/obmalloc.c)

```
layer 3: Object-specific memory(int/dict/list/string....)
		python 实现并维护
		用户对Python对象的直接操作，主要是各类特定对象的缓冲池机制，缓冲池，比如小整数对象池等等
layer 2: Python's object allocator
		实现了创建/销毁python对象的接口(PyObject_New/Del),涉及对象参数/引用计数等

layer 1: Python's raw memory allocator (PyMem_ API)
		包装了第0层的内存管理接口，提供同一个raw memory管理接口
		封装的原因：不同操作系统C行为不一致，保证可移植性，相同语义相同行为
		
layer 0: Underlying general-purpose allocator (ex: C library malloc)
		操作系统提供的内存管理接口，由操作系统实现并管理，Python不能干涉这一层的行为,大内存 分配调用malloc函数分配内存
```



## Python 内存分配策略之-block,pool

Python中有分为大内存和小内存，512K为分界线

- 大内存使用系统malloc进行分配

- 小内存使用python内存池进行分配

```
1. 如果要分配的内存空间大于 SMALL_REQUEST_THRESHOLD bytes(512 bytes), 将直接使用layer 1的内存分配接口进行分配
2. 否则, 使用不同的block来满足分配需求
```



> ```
> 申请一块大小28字节的内存, 实际从内存中划到32字节的一个block (从size class index为3的pool里面划出)
> ```

### block

内存块block 是python内存的最小单位

```c++
* For small requests we have the following table:
 *
 * Request in bytes     Size of allocated block      Size class idx
 * ----------------------------------------------------------------
 *        1-8                     8                       0
 *        9-16                   16                       1
 *       17-24                   24                       2
 *       25-32                   32                       3
 *       33-40                   40                       4
 *       41-48                   48                       5
 *       49-56                   56                       6
 *       57-64                   64                       7
 *       65-72                   72                       8
 *        ...                   ...                     ...
 *      497-504                 504                      62
 *      505-512                 512                      63
 *
 *      0, SMALL_REQUEST_THRESHOLD + 1 and up: routed to the underlying
 *      allocator.
 */
```

### pool

pool内存池，管理block, **一个pool管理着一堆固定大小的内存块**，在Python中, 一个pool的大小通常为一个**系统内存页. 4kB**

```c++
#define SYSTEM_PAGE_SIZE        (4 * 1024)
#define SYSTEM_PAGE_SIZE_MASK   (SYSTEM_PAGE_SIZE - 1)

#define POOL_SIZE               SYSTEM_PAGE_SIZE        /* must be 2^N */
#define POOL_SIZE_MASK          SYSTEM_PAGE_SIZE_MASK
```

*pool的4kB内存 = pool_header + block集合(N多大小一样的block)*

```c++
typedef uint8_t block;

/* Pool for small blocks. */
struct pool_header {
    union { block *_padding;
            uint count; } ref;          /* number of allocated blocks    */
    block *freeblock;                   /* pool's free list head         */
    struct pool_header *nextpool;       /* next pool of this size class  */
    struct pool_header *prevpool;       /* previous pool       ""        */
    uint arenaindex;                    /* index into arenas of base adr */
    uint szidx;                         /* block size class index        */
    uint nextoffset;                    /* bytes to virgin block         */
    uint maxnextoffset;                 /* largest valid nextoffset      */
};
```

pool_header 作用

```
与其他pool链接, 组成双向链表
2. 维护pool中可用的block, 单链表
3. 保存 szidx , 这个和该pool中block的大小有关系, (block size=8, szidx=0), (block size=16, szidx=1)...用于内存分配时匹配到拥有对应大小block的pool
```

![image.png](https://i.loli.net/2020/06/06/CJ9MnOGEm5THDBK.png)



### pool 初始化

```c++
void *
PyObject_Malloc(size_t nbytes)
{
  ...

          init_pool:
            // 1. 连接到 used_pools 双向链表, 作为表头
            // 注意, 这里 usedpools[0] 保存着 block size = 8 的所有used_pools的表头
            /* Frontlink to used pools. */
            next = usedpools[size + size]; /* == prev */
            pool->nextpool = next;
            pool->prevpool = next;
            next->nextpool = pool;
            next->prevpool = pool;
            pool->ref.count = 1;

            // 如果已经初始化过了...这里看初始化, 跳过
            if (pool->szidx == size) {
                /* Luckily, this pool last contained blocks
                 * of the same size class, so its header
                 * and free list are already initialized.
                 */
                bp = pool->freeblock;
                pool->freeblock = *(block **)bp;
                UNLOCK();
                return (void *)bp;
            }


            /*
             * Initialize the pool header, set up the free list to
             * contain just the second block, and return the first
             * block.
             */
            // 开始初始化pool_header
            // 这里 size = (uint)(nbytes - 1) >> ALIGNMENT_SHIFT;  其实是Size class idx, 即szidx
            pool->szidx = size;

            // 计算获得每个block的size
            size = INDEX2SIZE(size);

            // 注意 #define POOL_OVERHEAD           ROUNDUP(sizeof(struct pool_header))
            // bp => 初始化为pool + pool_header size,  跳过pool_header的内存
            bp = (block *)pool + POOL_OVERHEAD;

            // 计算偏移量, 这里的偏移量是绝对值
            // #define POOL_SIZE               SYSTEM_PAGE_SIZE        /* must be 2^N */
            // POOL_SIZE = 4kb, POOL_OVERHEAD = pool_header size
            // 下一个偏移位置: pool_header size + 2 * size
            pool->nextoffset = POOL_OVERHEAD + (size << 1);
            // 4kb - size
            pool->maxnextoffset = POOL_SIZE - size;

            // freeblock指向 bp + size = pool_header size + size
            pool->freeblock = bp + size;

            // 赋值NULL
            *(block **)(pool->freeblock) = NULL;
            UNLOCK();
            return (void *)bp;
        }
```



![image.png](https://i.loli.net/2020/06/06/Du96sNnrCxFyI3S.png)





### pool 进行block分配 - 总体代码

```c++
  if (pool != pool->nextpool) {   //
            /*
             * There is a used pool for this size class.
             * Pick up the head block of its free list.
             */
            ++pool->ref.count;
            bp = pool->freeblock; // 指针指向空闲block起始位置
            assert(bp != NULL);

            // 代码-1
            // 调整 pool->freeblock (假设A节点)指向链表下一个, 即bp首字节指向的下一个节点(假设B节点) , 如果此时!= NULL
            // 表示 A节点可用, 直接返回
            if ((pool->freeblock = *(block **)bp) != NULL) {
                UNLOCK();
                return (void *)bp;
            }

            // 代码-2
            /*
             * Reached the end of the free list, try to extend it.
             */
            // 有足够的空间, 分配一个, pool->freeblock 指向后移
            if (pool->nextoffset <= pool->maxnextoffset) {
                /* There is room for another block. */
                // 变更位置信息
                pool->freeblock = (block*)pool +
                                  pool->nextoffset;
                pool->nextoffset += INDEX2SIZE(size);


                *(block **)(pool->freeblock) = NULL; // 注意, 指向NULL
                UNLOCK();

                // 返回bp
                return (void *)bp;
            }

            // 代码-3
            /* Pool is full, unlink from used pools. */  // 满了, 需要从下一个pool获取
            next = pool->nextpool;
            pool = pool->prevpool;
            next->prevpool = pool;
            pool->nextpool = next;
            UNLOCK();
            return (void *)bp;
        }
```

### pool进行block分配 -1

内存块尚未分配完, 且此时不存在回收的block, 全新进来的时候, 分配第一块block

> ```c
> (pool->freeblock = *(block **)bp) == NULL
> ```

当进入**代码逻辑2**时，表示有空闲的block, 代码2的执行流程图如下

![image.png](https://i.loli.net/2020/06/06/JR3pP9cGQEveXbn.png)

### pool进行block分配 - 2 回收了某几个block

回收涉及的代码：

```c++
void
PyObject_Free(void *p)
{
    poolp pool;
    block *lastfree;
    poolp next, prev;
    uint size;

    pool = POOL_ADDR(p);
    if (Py_ADDRESS_IN_RANGE(p, pool)) {
        /* We allocated this address. */
        LOCK();
        /* Link p to the start of the pool's freeblock list.  Since
         * the pool had at least the p block outstanding, the pool
         * wasn't empty (so it's already in a usedpools[] list, or
         * was full and is in no list -- it's not in the freeblocks
         * list in any case).
         */
        assert(pool->ref.count > 0);            /* else it was empty */
        // p被释放, p的第一个字节值被设置为当前freeblock的值
        *(block **)p = lastfree = pool->freeblock;
        // freeblock被更新为指向p的首地址
        pool->freeblock = (block *)p;

        // 相当于往list中头插入了一个节点

     ...
    }
}
```

每释放一个block，该blcok就会变成`pool->freeblock`的头结点， 假设已经连续分配了5块, 第1块和第4块被释放，此时的内存图示如下：

![image.png](https://i.loli.net/2020/06/06/9cMYegzjWnwtfIh.png)

*此时再一个block分配调用进来, 执行分配, 进入的逻辑是`代码-1`*

```c++
bp = pool->freeblock; // 指针指向空闲block起始位置
// 代码-1
// 调整 pool->freeblock (假设A节点)指向链表下一个, 即bp首字节指向的下一个节点(假设B节点) , 如果此时!= NULL
// 表示 A节点可用, 直接返回
if ((pool->freeblock = *(block **)bp) != NULL) {
    UNLOCK();
    return (void *)bp;
}
```

![image.png](https://i.loli.net/2020/06/06/QdxnhDNbgwe7SGv.png)

### pool进行block分配 - 3 pool用完了

pool中内存空间都用完了, 进入`代码-3`

```c++
/* Pool is full, unlink from used pools. */  // 满了, 需要从下一个pool获取
next = pool->nextpool;
pool = pool->prevpool;
next->prevpool = pool;
pool->nextpool = next;
UNLOCK();
return (void *)bp;
```



## Python 内存分配策略之-arena

arena: 多个pool聚合的结果, 可放置64个pool

```c++
#define ARENA_SIZE              (256 << 10)     /* 256KB */
```

### arena结构

*一个完整的arena = arena_object + pool集合*

```c++
/* Record keeping for arenas. */
struct arena_object {
    /* The address of the arena, as returned by malloc.  Note that 0
     * will never be returned by a successful malloc, and is used
     * here to mark an arena_object that doesn't correspond to an
     * allocated arena.
     */
    uintptr_t address;

    /* Pool-aligned pointer to the next pool to be carved off. */
    block* pool_address;

    /* The number of available pools in the arena:  free pools + never-
     * allocated pools.
     */
    uint nfreepools;

    /* The total number of pools in the arena, whether or not available. */
    uint ntotalpools;

    /* Singly-linked list of available pools. */
    struct pool_header* freepools;

    /* Whenever this arena_object is not associated with an allocated
     * arena, the nextarena member is used to link all unassociated
     * arena_objects in the singly-linked `unused_arena_objects` list.
     * The prevarena member is unused in this case.
     *
     * When this arena_object is associated with an allocated arena
     * with at least one available pool, both members are used in the
     * doubly-linked `usable_arenas` list, which is maintained in
     * increasing order of `nfreepools` values.
     *
     * Else this arena_object is associated with an allocated arena
     * all of whose pools are in use.  `nextarena` and `prevarena`
     * are both meaningless in this case.
     */
    struct arena_object* nextarena;
    struct arena_object* prevarena;
};
```

```
arena_object的作用
1. 与其他arena连接, 组成双向链表
2. 维护arena中可用的pool, 单链表
```

- **pool_header和管理的blocks内存是一块连续的内存** => pool_header被申请时，其管理的的block集合的内存一并被申请 `uint maxnextoffset;         /* largest valid nextoffset   */`
- **arena_object 和其管理的内存是分离的** => arena_object被申请时，其管理的pool集合的内存没有被申请，而是在某一时刻建立关系的

![image.png](https://i.loli.net/2020/06/06/KudLt76QrnaXVie.png)

### arena的两种状态

```c
/* The head of the singly-linked, NULL-terminated list of available
 * arena_objects.
 */
// 单链表
static struct arena_object* unused_arena_objects = NULL;

/* The head of the doubly-linked, NULL-terminated at each end, list of
 * arena_objects associated with arenas that have pools available.
 */
// 双向链表
static struct arena_object* usable_arenas = NULL;
```

### arena 初始化

```c
* Allocate a new arena.  If we run out of memory, return NULL.  Else
 * allocate a new arena, and return the address of an arena_object
 * describing the new arena.  It's expected that the caller will set
 * `usable_arenas` to the return value.
 */
static struct arena_object*
new_arena(void)
{
    struct arena_object* arenaobj;
    uint excess;        /* number of bytes above pool alignment */
    void *address;
    static int debug_stats = -1;

    if (debug_stats == -1) {
        const char *opt = Py_GETENV("PYTHONMALLOCSTATS");
        debug_stats = (opt != NULL && *opt != '\0');
    }
    if (debug_stats)
        _PyObject_DebugMallocStats(stderr);

    // 判断是否需要扩充"未使用"的arena_object列表
    if (unused_arena_objects == NULL) {
        uint i;
        uint numarenas;
        size_t nbytes;

        /* Double the number of arena objects on each allocation.
         * Note that it's possible for `numarenas` to overflow.
         */
        // 确定需要申请的个数, 首次初始化, 16, 之后每次翻倍
        numarenas = maxarenas ? maxarenas << 1 : INITIAL_ARENA_OBJECTS;
        if (numarenas <= maxarenas)
            return NULL;                /* overflow */
#if SIZEOF_SIZE_T <= SIZEOF_INT
        if (numarenas > SIZE_MAX / sizeof(*arenas))
            return NULL;                /* overflow */
#endif
        nbytes = numarenas * sizeof(*arenas);
        // 申请内存
        arenaobj = (struct arena_object *)PyMem_RawRealloc(arenas, nbytes);
        if (arenaobj == NULL)
            return NULL;
        arenas = arenaobj;

        /* We might need to fix pointers that were copied.  However,
         * new_arena only gets called when all the pages in the
         * previous arenas are full.  Thus, there are *no* pointers
         * into the old array. Thus, we don't have to worry about
         * invalid pointers.  Just to be sure, some asserts:
         */
        assert(usable_arenas == NULL);
        assert(unused_arena_objects == NULL);

        /* Put the new arenas on the unused_arena_objects list. */
        for (i = maxarenas; i < numarenas; ++i) {
            arenas[i].address = 0;              /* mark as unassociated */
            // 新申请的一律为0, 标识着这个arena处于"未使用"
            arenas[i].nextarena = i < numarenas - 1 ?
                                   &arenas[i+1] : NULL;
        }

         // 将其放入unused_arena_objects链表中
        // unused_arena_objects 为新分配内存空间的开头
        /* Update globals. */
        unused_arena_objects = &arenas[maxarenas];
        maxarenas = numarenas;
    }

    /* Take the next available arena object off the head of the list. */
    assert(unused_arena_objects != NULL);
    // 从unused_arena_objects中, 获取一个未使用的object
    arenaobj = unused_arena_objects;
    unused_arena_objects = arenaobj->nextarena;  // 更新链表
    assert(arenaobj->address == 0);
    // 申请内存, 256KB, 内存地址赋值给arena的address. 这块内存可用
    address = _PyObject_Arena.alloc(_PyObject_Arena.ctx, ARENA_SIZE);
    if (address == NULL) {
        /* The allocation failed: return NULL after putting the
         * arenaobj back.
         */
        arenaobj->nextarena = unused_arena_objects;
        unused_arena_objects = arenaobj;
        return NULL;
    }
    arenaobj->address = (uintptr_t)address;

    ++narenas_currently_allocated;
    ++ntimes_arena_allocated;
    if (narenas_currently_allocated > narenas_highwater)
        narenas_highwater = narenas_currently_allocated;
    arenaobj->freepools = NULL;
    /* pool_address <- first pool-aligned address in the arena
       nfreepools <- number of whole pools that fit after alignment */
    arenaobj->pool_address = (block*)arenaobj->address;
    arenaobj->nfreepools = MAX_POOLS_IN_ARENA;
    // 将pool的起始地址调整为系统页的边界
    // 申请到 256KB, 放弃了一些内存, 而将可使用的内存边界pool_address调整到了与系统页对齐
    excess = (uint)(arenaobj->address & POOL_SIZE_MASK);
    if (excess != 0) {
        --arenaobj->nfreepools;
        arenaobj->pool_address += POOL_SIZE - excess;
    }
    arenaobj->ntotalpools = arenaobj->nfreepools;

    return arenaobj;
}
```

![image.png](https://i.loli.net/2020/06/06/KT5iJs4MXRqfYWZ.png)

从arenas取一个arena进行初始化

![image.png](https://i.loli.net/2020/06/06/dMJzhvcGpHXt978.png)

### arena分配 

new一个全新的arena

```c
static void*
pymalloc_alloc(void *ctx, size_t nbytes)
 {
            // 刚开始没有可用的arena
            if (usable_arenas == NULL) {
              // new一个, 作为双向链表的表头
              usable_arenas = new_arena();
              if (usable_arenas == NULL) {
                  UNLOCK();
                  goto redirect;
              }

              usable_arenas->nextarena =
                  usable_arenas->prevarena = NULL;

           }

          .......

          // 从arena中获取一个pool
          pool = (poolp)usable_arenas->pool_address;
          assert((block*)pool <= (block*)usable_arenas->address +
                                 ARENA_SIZE - POOL_SIZE);
          pool->arenaindex = usable_arenas - arenas;
          assert(&arenas[pool->arenaindex] == usable_arenas);
          pool->szidx = DUMMY_SIZE_IDX;

          // 更新 pool_address 向下一个节点
          usable_arenas->pool_address += POOL_SIZE;
          // 可用节点数量-1
          --usable_arenas->nfreepools;

}
```

从全新的arena中获取一个pool

![image.png](https://i.loli.net/2020/06/06/qPDIdJHRyUQ38x6.png)



假设arena是旧的, 怎么分配的pool, **跟pool分配block原理一样，使用单链表记录freepools**

```c
pool = usable_arenas->freepools;
if (pool != NULL) {
```

当arena中一整块pool被释放的时候

```c
/* Free a memory block allocated by pymalloc_alloc().
   Return 1 if it was freed.
   Return 0 if the block was not allocated by pymalloc_alloc(). */
static int
pymalloc_free(void *ctx, void *p) {
    struct arena_object* ao;
    uint nf;  /* ao->nfreepools */

    /* Link the pool to freepools.  This is a singly-linked
               * list, and pool->prevpool isn't used there.
              */
    ao = &arenas[pool->arenaindex];
    pool->nextpool = ao->freepools;
    ao->freepools = pool;
    nf = ++ao->nfreepools;
}
```

在pool整块被释放的时候, 会将pool加入到`arena->freepools`作为单链表的表头, 然后, 在从非全新arena中分配pool时, 优先从`arena->freepools`里面取, 如果取不到, 再从arena内存块里面获取

![image.png](https://i.loli.net/2020/06/06/GCkbIozLTwQXc7F.png)

**注: 上图中nfreepools = n - 2**

当arena1用完了，获取arena1指向的下一个节点arena2

```c
static void*
pymalloc_alloc(void *ctx, size_t nbytes)
{


          // 当发现用完了最后一个pool!!!!!!!!!!!
          // nfreepools = 0
          if (usable_arenas->nfreepools == 0) {
              assert(usable_arenas->nextarena == NULL ||
                     usable_arenas->nextarena->prevarena ==
                     usable_arenas);
              /* Unlink the arena:  it is completely allocated. */

              // 找到下一个节点!
              usable_arenas = usable_arenas->nextarena;
              // 右下一个
              if (usable_arenas != NULL) {
                  usable_arenas->prevarena = NULL; // 更新下一个节点的prevarens
                  assert(usable_arenas->address != 0);
              }
              // 没有下一个, 此时 usable_arenas = NULL, 下次进行内存分配的时候, 就会从arenas数组中取一个

          }

  }
```

注意: 这里有个逻辑, 就是每分配一个pool, 就检查是不是用到了最后一个, 如果是, 需要变更`usable_arenas`到下一个可用的节点, 如果没有可用的, 那么下次进行内存分配的时候, 会判定从arenas数组中取一个

###　arena回收

内存分配和回收最小单位是block, 当一个block被回收的时候, 可能触发pool被回收, pool被回收, 将会触发arena的回收机制

- 1. arena中所有pool都是闲置的(empty), 将arena内存释放, 返回给操作系统

- 2. 如果arena中之前所有的pool都是占用的(used), 现在释放了一个pool(empty), 需要将 arena加入到usable_arenas, 会加入链表表头
- 3. 如果arena中empty的pool个数n, 则从useable_arenas开始寻找可以插入的位置. 将arena插入. (**useable_arenas是一个有序链表, 按empty pool的个数, 保证empty pool数量越多, 被使用的几率越小, 最终被整体释放的机会越大**)

### 内存分配的步骤

**关注点：如何寻找到一块可用的nbytes的blcok内存？**

> pool = usedpools[size + size]
>
> if pool:
>
> ​	pool 没满，取一个blcok返回
>
> ​	pool 满了，从下一个pool取一个blcok返回
>
> else:
>
> ​	获取arena, 从里面初始化一个pool, 拿到第一个blcok返回

**进行内存分配和销毁, 所有操作都是在pool上进行的**



> **问题:** pool中所有block的size一样, 但是在arena中, 每个pool的size都可能不一样, 那么最终这些pool是怎么维护的? 怎么根据大小找到需要的block所在的pool? => `usedpools`

## pool在内存池中的三种状态

1. used状态：pool中至少有一个block已经被使用，并且至少有一个block未被使用，这种状态的pool受控于Python内部维护的usedpool数组
2. full状态：pool中所有的block都已经被使用，这种状态的pool在arena中, 但不在arena的freepools链表中，处于full的pool各自独立, 不会被链表维护起来
3. empty状态：pool中所有的blcok都未被使用，处于这个状态的pool的集合通过其pool_header中的nextpool构成一个链表，链表的表头示arena_object中的freepools

![image.png](https://i.loli.net/2020/06/06/g3moVC27ERrkFv8.png)

Python内部维护的usedpools数组是一个非常巧妙的实现，维护着所有的处于used状态的pool，当申请内存时，python就会通过usedpools寻找到一个可用的pool`(处于used状态)`，从中分配一个block。因此我们想，一定有一个usedpools相关联的机制，完成从申请的内存的大小到size class index之间的转换，否则python就无法找到最合适的pool了。这种机制和usedpools的结构有着密切的关系，我们看一下它的结构

### usedpools

usedpools数组: 维护着所有处于used状态的pool, 当申请内存的时候, 会通过usedpools寻找到一块可用的(处于used状态的)pool, 从中分配一个block。

```c
//obmalloc.c
typedef uint8_t block;
#define PTA(x)  ((poolp )((uint8_t *)&(usedpools[2*(x)]) - 2*sizeof(block *)))
#define PT(x)   PTA(x), PTA(x)

//在我当前的机器就是512/8=64个，对应的size class index就是从0到63
#define NB_SMALL_SIZE_CLASSES   (SMALL_REQUEST_THRESHOLD / ALIGNMENT)

static poolp usedpools[2 * ((NB_SMALL_SIZE_CLASSES + 7) / 8) * 8] = {
    PT(0), PT(1), PT(2), PT(3), PT(4), PT(5), PT(6), PT(7)
#if NB_SMALL_SIZE_CLASSES > 8
    , PT(8), PT(9), PT(10), PT(11), PT(12), PT(13), PT(14), PT(15)
#if NB_SMALL_SIZE_CLASSES > 16
    , PT(16), PT(17), PT(18), PT(19), PT(20), PT(21), PT(22), PT(23)
#if NB_SMALL_SIZE_CLASSES > 24
    , PT(24), PT(25), PT(26), PT(27), PT(28), PT(29), PT(30), PT(31)
#if NB_SMALL_SIZE_CLASSES > 32
    , PT(32), PT(33), PT(34), PT(35), PT(36), PT(37), PT(38), PT(39)
#if NB_SMALL_SIZE_CLASSES > 40
    , PT(40), PT(41), PT(42), PT(43), PT(44), PT(45), PT(46), PT(47)
#if NB_SMALL_SIZE_CLASSES > 48
    , PT(48), PT(49), PT(50), PT(51), PT(52), PT(53), PT(54), PT(55)
#if NB_SMALL_SIZE_CLASSES > 56
    , PT(56), PT(57), PT(58), PT(59), PT(60), PT(61), PT(62), PT(63)
#if NB_SMALL_SIZE_CLASSES > 64
#error "NB_SMALL_SIZE_CLASSES should be less than 64"
#endif /* NB_SMALL_SIZE_CLASSES > 64 */
#endif /* NB_SMALL_SIZE_CLASSES > 56 */
#endif /* NB_SMALL_SIZE_CLASSES > 48 */
#endif /* NB_SMALL_SIZE_CLASSES > 40 */
#endif /* NB_SMALL_SIZE_CLASSES > 32 */
#endif /* NB_SMALL_SIZE_CLASSES > 24 */
#endif /* NB_SMALL_SIZE_CLASSES > 16 */
#endif /* NB_SMALL_SIZE_CLASSES >  8 */
};

```



![image.png](https://i.loli.net/2020/06/06/5pPzyvVek6cHiG3.png)

如果正在申请28字节， python首先会获取(size class index) ` size = (uint )(nbytes - 1) >> ALIGNMENT_SHIFT` 显然这里`size=3`， 那么在usedpools中，寻找第3+3=6个元素，发现usedpools[6]的值是指向usedpools[4]的地址

```c
//obmalloc.c
/* Pool for small blocks. */
struct pool_header {
    union { block *_padding;
            uint count; } ref;          /* 当然pool里面的block数量    */
    block *freeblock;                   /* 一个链表，指向下一个可用的block   */
    struct pool_header *nextpool;       /* 指向下一个pool  */
    struct pool_header *prevpool;       /* 指向上一个pool       ""        */
    uint arenaindex;                    /* 在area里面的索引 */
    uint szidx;                         /* block的大小(固定值？后面说)     */
    uint nextoffset;                    /* 下一个可用block的内存偏移量         */
    uint maxnextoffset;                 /* 最后一个block距离开始位置的距离     */
};

```

>  显然是从usedpools[6]`(即usedpools+4)`开始向后偏移8个字节(一个ref的大小加上一个freeblock的大小)后的内存，正好是usedpools[6]的地址`(即usedpools+6)`，这是python内部的trick

当我们要申请一个size class为32字节的pool，想要将其放入这个usedpools中时，要怎么做呢？从上面的描述我们知道，只需要进行`usedpools[i+i] -> nextpool = pool`即可，其中i为size class index，对应于32字节，这个i为3.当下次需要访问size class 为32字节`(size class index为3)`的pool时，只需要简单地访问usedpools[3+3]就可以得到了。python正是使用这个usedpools快速地从众多的pool中快速地寻找到一个最适合当前内存需求的pool，从中分配一块block。

```c
//obmalloc.c
static int
pymalloc_alloc(void *ctx, void **ptr_p, size_t nbytes)
{
    block *bp;
    poolp pool;
    poolp next;
    uint size;
    ...
    LOCK();
    //获得size class index
    size = (uint)(nbytes - 1) >> ALIGNMENT_SHIFT;
    //直接通过usedpools[size+size]，这里的size不就是我们上面说的i吗？
    pool = usedpools[size + size];
    //如果usedpools中有可用的pool
    if (pool != pool->nextpool) {
        ... //有可用pool
    }
    ... //无可用pool，尝试获取empty状态的pool
}  
```

### 内存池全局结构

![image.png](https://i.loli.net/2020/06/06/81sVxBNoFSKXlwh.png)



参考: 

[pyhton源码阅读-内存管理机制](http://wklken.me/posts/2015/08/29/python-source-memory-2.html)

[python源码解析第17章-python内存管理与垃圾回收](https://www.cnblogs.com/traditional/p/12202429.html)



后期查缺补漏需要看的文章

[Memory management by Zpoint](https://github.com/zpoint/CPython-Internals/blob/master/Interpreter/memory_management/memory_management_cn.md)

[Memory management in Python](https://rushter.com/blog/python-memory-managment/)