/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_Alloc">lua_Alloc</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_Alloc
/// 		typedef void * (*lua_Alloc) (void *ud,
/// 		                             void *ptr,
/// 		                             size_t osize,
/// 		                             size_t nsize);
/// 		
/// 		Lua 状态机中使用的内存分配器函数的类型。
/// 		内存分配函数必须提供一个功能类似于 realloc 但又不完全相同的函数。
/// 		它的参数有
/// 		ud ，一个由 lua_newstate 传给它的指针；
/// 		ptr ，一个指向已分配出来或是将被重新分配或是要释放的内存块指针；
/// 		osize ，内存块原来的尺寸；
/// 		nsize ，新内存块的尺寸。
/// 		如果且只有 osize 是零时，ptr 为 NULL 。
/// 		当 nsize 是零，分配器必须返回 NULL；
/// 		如果 osize 不是零，分配器应当释放掉 ptr 指向的内存块。
/// 		当 nsize 不是零，若分配器不能满足请求时，分配器返回 NULL 。
/// 		当 nsize 不是零而 osize 是零时，分配器应该和 malloc
/// 		有相同的行为。
/// 		当 nsize 和 osize 都不是零时，分配器则应和 realloc
/// 		保持一样的行为。
/// 		Lua 假设分配器在 osize >= nsize 时永远不会失败。
/// 		
/// 		这里有一个简单的分配器函数的实现。
/// 		这个实现被放在补充库中，由 luaL_newstate 提供。
/// 		
/// 		     static void *l_alloc (void *ud, void *ptr, size_t osize,
/// 		                                                size_t nsize) {
/// 		       (void)ud;  (void)osize;  /* not used */
/// 		       if (nsize == 0) {
/// 		         free(ptr);
/// 		         return NULL;
/// 		       }
/// 		       else
/// 		         return realloc(ptr, nsize);
/// 		     }
/// 		
/// 		这段代码假设 free(NULL) 啥也不影响，而且
/// 		realloc(NULL, size) 等价于 malloc(size)。
/// 		这两点是 ANSI C 保证的行为。
/// 		
/// 	</para>
/// </remarks>
public void lua_Alloc()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_atpanic">lua_atpanic</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_atpanic
/// 		lua_CFunction lua_atpanic (lua_State *L, lua_CFunction panicf);
/// 		
/// 		设置一个新的 panic （恐慌） 函数，并返回前一个。
/// 		
/// 		如果在保护环境之外发生了任何错误，
/// 		Lua 就会调用一个 panic 函数，接着调用 exit(EXIT_FAILURE)，
/// 		这样就开始退出宿主程序。
/// 		你的 panic 函数可以永远不返回（例如作一次长跳转）来避免程序退出。
/// 		
/// 		panic 函数可以从栈顶取到出错信息。
/// 		
/// 	</para>
/// </remarks>
public void lua_atpanic()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_call">lua_call</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_call
/// 		void lua_call (lua_State *L, int nargs, int nresults);
/// 		
/// 		调用一个函数。
/// 		
/// 		要调用一个函数请遵循以下协议：
/// 		首先，要调用的函数应该被压入堆栈；
/// 		接着，把需要传递给这个函数的参数按正序压栈；
/// 		这是指第一个参数首先压栈。
/// 		最后调用一下 lua_call；
/// 		nargs 是你压入堆栈的参数个数。
/// 		当函数调用完毕后，所有的参数以及函数本身都会出栈。
/// 		而函数的返回值这时则被压入堆栈。
/// 		返回值的个数将被调整为 nresults 个，
/// 		除非 nresults 被设置成 LUA_MULTRET。
/// 		在这种情况下，所有的返回值都被压入堆栈中。
/// 		Lua 会保证返回值都放入栈空间中。
/// 		函数返回值将按正序压栈（第一个返回值首先压栈），
/// 		因此在调用结束后，最后一个返回值将被放在栈顶。
/// 		
/// 		被调用函数内发生的错误将（通过 longjmp）一直上抛。
/// 		
/// 		下面的例子中，这行 Lua 代码等价于在宿主程序用 C 代码做一些工作：
/// 		
/// 		     a = f("how", t.x, 14)
/// 		
/// 		这里是 C 里的代码：
/// 		
/// 		     lua_getfield(L, LUA_GLOBALSINDEX, "f");          /* 将调用的函数 */
/// 		     lua_pushstring(L, "how");                          /* 第一个参数 */
/// 		     lua_getfield(L, LUA_GLOBALSINDEX, "t");          /* table 的索引 */
/// 		     lua_getfield(L, -1, "x");         /* 压入 t.x 的值（第 2 个参数）*/
/// 		     lua_remove(L, -2);                           /* 从堆栈中移去 't' */
/// 		     lua_pushinteger(L, 14);                           /* 第 3 个参数 */
/// 		     lua_call(L, 3, 1); /* 调用 'f'，传入 3 个参数，并索取 1 个返回值 */
/// 		     lua_setfield(L, LUA_GLOBALSINDEX, "a");      /* 设置全局变量 'a' */
/// 		
/// 		注意上面这段代码是“平衡”的：
/// 		到了最后，堆栈恢复成原由的配置。
/// 		这是一种良好的编程习惯。
/// 		
/// 	</para>
/// </remarks>
public void lua_call()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_CFunction">lua_CFunction</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_CFunction
/// 		typedef int (*lua_CFunction) (lua_State *L);
/// 		
/// 		C 函数的类型。
/// 		
/// 		为了正确的和 Lua 通讯，C 函数必须使用下列
/// 		定义了参数以及返回值传递方法的协议：
/// 		C 函数通过 Lua 中的堆栈来接受参数，参数以正序入栈（第一个参数首先入栈）。
/// 		因此，当函数开始的时候，
/// 		lua_gettop(L) 可以返回函数收到的参数个数。
/// 		第一个参数（如果有的话）在索引 1 的地方，而最后一个参数在索引 lua_gettop(L) 处。
/// 		当需要向 Lua 返回值的时候，C 函数只需要把它们以正序压到堆栈上（第一个返回值最先压入），
/// 		然后返回这些返回值的个数。
/// 		在这些返回值之下的，堆栈上的东西都会被 Lua 丢掉。
/// 		和 Lua 函数一样，从 Lua 中调用 C 函数也可以有很多返回值。
/// 		
/// 		下面这个例子中的函数将接收若干数字参数，并返回它们的平均数与和：
/// 		
/// 		     static int foo (lua_State *L) {
/// 		       int n = lua_gettop(L);    /* 参数的个数 */
/// 		       lua_Number sum = 0;
/// 		       int i;
/// 		       for (i = 1; i <= n; i++) {
/// 		         if (!lua_isnumber(L, i)) {
/// 		           lua_pushstring(L, "incorrect argument");
/// 		           lua_error(L);
/// 		         }
/// 		         sum += lua_tonumber(L, i);
/// 		       }
/// 		       lua_pushnumber(L, sum/n);   /* 第一个返回值 */
/// 		       lua_pushnumber(L, sum);     /* 第二个返回值 */
/// 		       return 2;                   /* 返回值的个数 */
/// 		     }
/// 		
/// 	</para>
/// </remarks>
public void lua_CFunction()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_checkstack">lua_checkstack</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_checkstack
/// 		int lua_checkstack (lua_State *L, int extra);
/// 		
/// 		确保堆栈上至少有 extra 个空位。
/// 		如果不能把堆栈扩展到相应的尺寸，函数返回 false 。
/// 		这个函数永远不会缩小堆栈；
/// 		如果堆栈已经比需要的大了，那么就放在那里不会产生变化。
/// 		
/// 	</para>
/// </remarks>
public void lua_checkstack()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_close">lua_close</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_close
/// 		void lua_close (lua_State *L);
/// 		
/// 		销毁指定 Lua 状态机中的所有对象（如果有垃圾收集相关的元方法的话，会调用它们），
/// 		并且释放状态机中使用的所有动态内存。
/// 		在一些平台上，你可以不必调用这个函数，
/// 		因为当宿主程序结束的时候，所有的资源就自然被释放掉了。
/// 		另一方面，长期运行的程序，比如一个后台程序或是一个 web 服务器，
/// 		当不再需要它们的时候就应该释放掉相关状态机。这样可以避免状态机扩张的过大。
/// 		
/// 	</para>
/// </remarks>
public void lua_close()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_concat">lua_concat</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_concat
/// 		void lua_concat (lua_State *L, int n);
/// 		
/// 		连接栈顶的 n 个值，
/// 		然后将这些值出栈，并把结果放在栈顶。
/// 		如果 n 为 1 ，结果就是一个字符串放在栈上（即，函数什么都不做）；
/// 		如果 n 为 0 ，结果是一个空串。
/// 		
/// 		连接依照 Lua 中创建语义完成（参见 §2.5.4 ）。
/// 		
/// 	</para>
/// </remarks>
public void lua_concat()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_cpcall">lua_cpcall</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_cpcall
/// 		int lua_cpcall (lua_State *L, lua_CFunction func, void *ud);
/// 		
/// 		以保护模式调用 C 函数 func 。
/// 		func 只有能从堆栈上拿到一个参数，就是包含有 ud 的 light userdata。
/// 		当有错误时，
/// 		lua_cpcall 返回和 lua_pcall 相同的错误代码，
/// 		并在栈顶留下错误对象；
/// 		否则它返回零，并不会修改堆栈。
/// 		所有从 func 内返回的值都会被扔掉。
/// 		
/// 	</para>
/// </remarks>
public void lua_cpcall()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_createtable">lua_createtable</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_createtable
/// 		void lua_createtable (lua_State *L, int narr, int nrec);
/// 		
/// 		创建一个新的空 table 压入堆栈。
/// 		这个新 table 将被预分配 narr 个元素的数组空间
/// 		以及 nrec 个元素的非数组空间。
/// 		当你明确知道表中需要多少个元素时，预分配就非常有用。
/// 		如果你不知道，可以使用函数 lua_newtable。
/// 		
/// 	</para>
/// </remarks>
public void lua_createtable()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_dump">lua_dump</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_dump
/// 		int lua_dump (lua_State *L, lua_Writer writer, void *data);
/// 		
/// 		把函数 dump 成二进制 chunk 。
/// 		函数接收栈顶的 Lua 函数做参数，然后生成它的二进制 chunk 。
/// 		若被 dump 出来的东西被再次加载，加载的结果就相当于原来的函数。
/// 		当它在产生 chunk 的时候，lua_dump 
/// 		通过调用函数 writer （参见 lua_Writer）
/// 		来写入数据，后面的 data 参数会被传入 writer 。
/// 		
/// 		最后一次由写入器 (writer) 返回值将作为这个函数的返回值返回；
/// 		0 表示没有错误。
/// 		
/// 		这个函数不会把 Lua 返回弹出堆栈。
/// 		
/// 	</para>
/// </remarks>
public void lua_dump()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_equal">lua_equal</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_equal
/// 		int lua_equal (lua_State *L, int index1, int index2);
/// 		
/// 		如果依照 Lua 中 == 操作符语义，索引 index1 和 index2
/// 		中的值相同的话，返回 1 。
/// 		否则返回 0 。
/// 		如果任何一个索引无效也会返回 0。
/// 		
/// 	</para>
/// </remarks>
public void lua_equal()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_error">lua_error</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_error
/// 		int lua_error (lua_State *L);
/// 		
/// 		产生一个 Lua 错误。
/// 		错误信息（实际上可以是任何类型的 Lua 值）必须被置入栈顶。
/// 		这个函数会做一次长跳转，因此它不会再返回。
/// 		（参见 luaL_error）。
/// 		
/// 	</para>
/// </remarks>
public void lua_error()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_gc">lua_gc</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_gc
/// 		int lua_gc (lua_State *L, int what, int data);
/// 		
/// 		控制垃圾收集器。
/// 		
/// 		这个函数根据其参数 what 发起几种不同的任务：
/// 		
/// 		• LUA_GCSTOP:
/// 		停止垃圾收集器。
/// 		
/// 		• LUA_GCRESTART:
/// 		重启垃圾收集器。
/// 		
/// 		• LUA_GCCOLLECT:
/// 		发起一次完整的垃圾收集循环。
/// 		
/// 		• LUA_GCCOUNT:
/// 		返回 Lua 使用的内存总量（以 K 字节为单位）。
/// 		
/// 		• LUA_GCCOUNTB:
/// 		返回当前内存使用量除以 1024 的余数。
/// 		
/// 		• LUA_GCSTEP:
/// 		发起一步增量垃圾收集。
/// 		步数由 data 控制（越大的值意味着越多步），
/// 		而其具体含义（具体数字表示了多少）并未标准化。
/// 		如果你想控制这个步数，必须实验性的测试
/// 		data 的值。
/// 		如果这一步结束了一个垃圾收集周期，返回返回 1 。
/// 		
/// 		• LUA_GCSETPAUSE:
/// 		把 data/100 设置为 garbage-collector pause 的新值（参见 §2.10）。
/// 		函数返回以前的值。
/// 		
/// 		• LUA_GCSETSTEPMUL:
/// 		把 arg/100 设置成 step multiplier （参见 §2.10）。
/// 		函数返回以前的值。
/// 		
/// 	</para>
/// </remarks>
public void lua_gc()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_getallocf">lua_getallocf</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_getallocf
/// 		lua_Alloc lua_getallocf (lua_State *L, void **ud);
/// 		
/// 		返回给定状态机的内存分配器函数。
/// 		如果 ud 不是 NULL ，Lua 把调用
/// 		lua_newstate 时传入的那个指针放入 *ud 。
/// 		
/// 	</para>
/// </remarks>
public void lua_getallocf()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_getfenv">lua_getfenv</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_getfenv
/// 		void lua_getfenv (lua_State *L, int index);
/// 		
/// 		把索引处值的环境表压入堆栈。
/// 		
/// 	</para>
/// </remarks>
public void lua_getfenv()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_getfield">lua_getfield</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_getfield
/// 		void lua_getfield (lua_State *L, int index, const char *k);
/// 		
/// 		把 t[k] 值压入堆栈，
/// 		这里的 t 是指有效索引 index 指向的值。
/// 		在 Lua 中，这个函数可能触发对应 "index" 事件的元方法
/// 		（参见 §2.8）。
/// 		
/// 	</para>
/// </remarks>
public void lua_getfield()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_getglobal">lua_getglobal</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_getglobal
/// 		void lua_getglobal (lua_State *L, const char *name);
/// 		
/// 		把全局变量 name 里的值压入堆栈。
/// 		这个是用一个宏定义出来的：
/// 		
/// 		     #define lua_getglobal(L,s)  lua_getfield(L, LUA_GLOBALSINDEX, s)
/// 		
/// 	</para>
/// </remarks>
public void lua_getglobal()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_getmetatable">lua_getmetatable</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_getmetatable
/// 		int lua_getmetatable (lua_State *L, int index);
/// 		
/// 		把给定索引指向的值的元表压入堆栈。
/// 		如果索引无效，或是这个值没有元表，
/// 		函数将返回 0 并且不会向栈上压任何东西。
/// 		
/// 	</para>
/// </remarks>
public void lua_getmetatable()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_gettable">lua_gettable</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_gettable
/// 		void lua_gettable (lua_State *L, int index);
/// 		
/// 		把 t[k] 值压入堆栈，
/// 		这里的 t 是指有效索引 index 指向的值，
/// 		而 k 则是栈顶放的值。
/// 		
/// 		这个函数会弹出堆栈上的 key （把结果放在栈上相同位置）。
/// 		在 Lua 中，这个函数可能触发对应 "index" 事件的元方法
/// 		（参见 §2.8）。
/// 		
/// 	</para>
/// </remarks>
public void lua_gettable()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_gettop">lua_gettop</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_gettop
/// 		int lua_gettop (lua_State *L);
/// 		
/// 		返回栈顶元素的索引。
/// 		因为索引是从 1 开始编号的，
/// 		所以这个结果等于堆栈上的元素个数（因此返回 0 表示堆栈为空）。
/// 		
/// 	</para>
/// </remarks>
public void lua_gettop()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_insert">lua_insert</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_insert
/// 		void lua_insert (lua_State *L, int index);
/// 		
/// 		把栈顶元素插入指定的有效索引处，
/// 		并依次移动这个索引之上的元素。
/// 		不要用伪索引来调用这个函数，
/// 		因为伪索引不是真正指向堆栈上的位置。
/// 		
/// 	</para>
/// </remarks>
public void lua_insert()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_Integer">lua_Integer</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_Integer
/// 		typedef ptrdiff_t lua_Integer;
/// 		
/// 		这个类型被用于 Lua API 接收整数值。
/// 		
/// 		缺省时这个被定义为 ptrdiff_t ，
/// 		这个东西通常是机器能处理的最大整数类型。
/// 		
/// 	</para>
/// </remarks>
public void lua_Integer()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_isboolean">lua_isboolean</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_isboolean
/// 		int lua_isboolean (lua_State *L, int index);
/// 		
/// 		当给定索引的值类型为 boolean 时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_isboolean()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_iscfunction">lua_iscfunction</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_iscfunction
/// 		int lua_iscfunction (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个 C 函数时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_iscfunction()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_isfunction">lua_isfunction</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_isfunction
/// 		int lua_isfunction (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个函数（ C 或 Lua 函数均可）时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_isfunction()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_islightuserdata">lua_islightuserdata</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_islightuserdata
/// 		int lua_islightuserdata (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个 light userdata 时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_islightuserdata()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_isnil">lua_isnil</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_isnil
/// 		int lua_isnil (lua_State *L, int index);
/// 		
/// 		当给定索引的值是 nil 时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_isnil()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_isnumber">lua_isnumber</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_isnumber
/// 		int lua_isnumber (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个数字，或是一个可转换为数字的字符串时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_isnumber()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_isstring">lua_isstring</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_isstring
/// 		int lua_isstring (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个字符串或是一个数字（数字总能转换成字符串）时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_isstring()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_istable">lua_istable</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_istable
/// 		int lua_istable (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个 table 时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_istable()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_isthread">lua_isthread</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_isthread
/// 		int lua_isthread (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个 thread 时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_isthread()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_isuserdata">lua_isuserdata</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_isuserdata
/// 		int lua_isuserdata (lua_State *L, int index);
/// 		
/// 		当给定索引的值是一个 userdata （无论是完整的 userdata 还是 light userdata ）时，返回 1 ，否则返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_isuserdata()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_lessthan">lua_lessthan</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_lessthan
/// 		int lua_lessthan (lua_State *L, int index1, int index2);
/// 		
/// 		如果索引 index1 处的值小于
/// 		索引 index2 处的值时，返回 1 ；
/// 		否则返回 0 。
/// 		其语义遵循 Lua 中的 < 操作符（就是说，有可能调用元方法）。
/// 		如果任何一个索引无效，也会返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_lessthan()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_load">lua_load</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_load
/// 		int lua_load (lua_State *L,
/// 		              lua_Reader reader,
/// 		              void *data,
/// 		              const char *chunkname);
/// 		
/// 		加载一个 Lua chunk 。
/// 		如果没有错误，
/// 		lua_load 把一个编译好的 chunk 作为一个
/// 		Lua 函数压入堆栈。
/// 		否则，压入出错信息。
/// 		lua_load 的返回值可以是：
/// 		
/// 		• 0: 没有错误；
/// 		
/// 		• LUA_ERRSYNTAX:
/// 		在预编译时碰到语法错误；
/// 		
/// 		• LUA_ERRMEM:
/// 		内存分配错误。
/// 		
/// 		这个函数仅仅加栽 chunk ；而不会去运行它。
/// 		
/// 		lua_load 会自动检测 chunk 是文本的还是二进制的，
/// 		然后做对应的加载操作（参见程序 luac）。
/// 		
/// 		lua_load 函数使用一个用户提供的 reader 函数来
/// 		读取 chunk （参见 lua_Reader）。
/// 		data 参数会被传入读取器函数。
/// 		
/// 		chunkname 这个参数可以赋予 chunk 一个名字，
/// 		这个名字被用于出错信息和调试信息（参见 §3.8）。
/// 		
/// 	</para>
/// </remarks>
public void lua_load()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_newstate">lua_newstate</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_newstate
/// 		lua_State *lua_newstate (lua_Alloc f, void *ud);
/// 		
/// 		创建的一个新的独立的状态机。
/// 		如果创建不了（因为内存问题）返回 NULL 。
/// 		参数 f 是一个分配器函数；
/// 		Lua 将通过这个函数做状态机内所有的内存分配操作。
/// 		第二个参数 ud ，这个指针将在每次调用分配器时被直接传入。
/// 		
/// 	</para>
/// </remarks>
public void lua_newstate()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_newtable">lua_newtable</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_newtable
/// 		void lua_newtable (lua_State *L);
/// 		
/// 		创建一个空 table ，并将之压入堆栈。
/// 		它等价于 lua_createtable(L, 0, 0) 。
/// 		
/// 	</para>
/// </remarks>
public void lua_newtable()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_newthread">lua_newthread</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_newthread
/// 		lua_State *lua_newthread (lua_State *L);
/// 		
/// 		创建一个新线程，并将其压入堆栈，
/// 		并返回维护这个线程的 lua_State 指针。
/// 		这个函数返回的新状态机共享原有状态机中的所有对象（比如一些 table），
/// 		但是它有独立的执行堆栈。
/// 		
/// 		没有显式的函数可以用来关闭或销毁掉一个线程。
/// 		线程跟其它 Lua 对象一样是垃圾收集的条目之一。
/// 		
/// 	</para>
/// </remarks>
public void lua_newthread()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_newuserdata">lua_newuserdata</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_newuserdata
/// 		void *lua_newuserdata (lua_State *L, size_t size);
/// 		
/// 		这个函数分配分配一块指定大小的内存块，
/// 		把内存块地址作为一个完整的 userdata 压入堆栈，并返回这个地址。
/// 		
/// 		userdata 代表 Lua 中的 C 值。
/// 		完整的 userdata 代表一块内存。
/// 		它是一个对象（就像 table 那样的对象）：
/// 		你必须创建它，它有着自己的元表，而且它在被回收时，可以被监测到。
/// 		一个完整的 userdata 只和它自己相等（在等于的原生作用下）。
/// 		
/// 		当 Lua 通过 gc 元方法回收一个完整的 userdata 时，
/// 		Lua 调用这个元方法并把 userdata 标记为已终止。
/// 		等到这个 userdata 再次被收集的时候，Lua 会释放掉相关的内存。
/// 		
/// 	</para>
/// </remarks>
public void lua_newuserdata()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_next">lua_next</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_next
/// 		int lua_next (lua_State *L, int index);
/// 		
/// 		从栈上弹出一个 key（键），
/// 		然后把索引指定的表中 key-value（健值）对压入堆栈
/// 		（指定 key 后面的下一 (next) 对）。
/// 		如果表中以无更多元素，
/// 		那么 lua_next 将返回 0 （什么也不压入堆栈）。
/// 		
/// 		典型的遍历方法是这样的：
/// 		
/// 		     /* table 放在索引 't' 处 */
/// 		     lua_pushnil(L);  /* 第一个 key */
/// 		     while (lua_next(L, t) != 0) {
/// 		       /* 用一下 'key' （在索引 -2 处） 和 'value' （在索引 -1 处） */
/// 		       printf("%s - %s\n",
/// 		              lua_typename(L, lua_type(L, -2)),
/// 		              lua_typename(L, lua_type(L, -1)));
/// 		       /* 移除 'value' ；保留 'key' 做下一次迭代 */
/// 		       lua_pop(L, 1);
/// 		     }
/// 		
/// 		在遍历一张表的时候，
/// 		不要直接对 key 调用 lua_tolstring ，
/// 		除非你知道这个 key 一定是一个字符串。
/// 		调用 lua_tolstring 有可能改变给定索引位置的值；
/// 		这会对下一次调用 lua_next 造成影响。
/// 		
/// 	</para>
/// </remarks>
public void lua_next()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_Number">lua_Number</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_Number
/// 		typedef double lua_Number;
/// 		
/// 		Lua 中数字的类型。
/// 		确省是 double ，但是你可以在 luaconf.h 中修改它。
/// 		
/// 		通过修改配置文件你可以改变 Lua 让它操作其它数字类型（例如：float 或是 long ）。
/// 		
/// 	</para>
/// </remarks>
public void lua_Number()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_objlen">lua_objlen</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_objlen
/// 		size_t lua_objlen (lua_State *L, int index);
/// 		
/// 		返回指定的索引处的值的长度。
/// 		对于 string ，那就是字符串的长度；
/// 		对于 table ，是取长度操作符 ('#') 的结果；
/// 		对于 userdata ，就是为其分配的内存块的尺寸；
/// 		对于其它值，为 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_objlen()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pcall">lua_pcall</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pcall
/// 		lua_pcall (lua_State *L, int nargs, int nresults, int errfunc);
/// 		
/// 		以保护模式调用一个函数。
/// 		
/// 		nargs 和 nresults 的含义与
/// 		lua_call 中的相同。
/// 		如果在调用过程中没有发生错误，
/// 		lua_pcall 的行为和 lua_call 完全一致。
/// 		但是，如果有错误发生的话，
/// 		lua_pcall 会捕获它，
/// 		然后把单一的值（错误信息）压入堆栈，然后返回错误码。
/// 		同 lua_call 一样，
/// 		lua_pcall 总是把函数本身和它的参数从栈上移除。
/// 		
/// 		如果 errfunc 是 0 ，
/// 		返回在栈顶的错误信息就和原始错误信息完全一致。
/// 		否则，errfunc 就被当成是错误处理函数在栈上的索引。
/// 		（在当前的实现里，这个索引不能是伪索引。）
/// 		在发生运行时错误时，
/// 		这个函数会被调用而参数就是错误信息。
/// 		错误处理函数的返回值将被 lua_pcall 作为出错信息返回在堆栈上。
/// 		
/// 		典型的用法中，错误处理函数被用来在出错信息上加上更多的调试信息，比如栈跟踪信息 (stack traceback) 。
/// 		这些信息在 lua_pcall 返回后，因为栈已经展开 (unwound) ，
/// 		所以收集不到了。
/// 		
/// 		lua_pcall 函数在调用成功时返回 0 ，
/// 		否则返回以下（定义在 lua.h 中的）错误代码中的一个：
/// 		
/// 		• LUA_ERRRUN:
/// 		运行时错误。
/// 		
/// 		• LUA_ERRMEM:
/// 		内存分配错误。
/// 		对于这种错，Lua 调用不了错误处理函数。
/// 		
/// 		• LUA_ERRERR:
/// 		在运行错误处理函数时发生的错误。
/// 		
/// 	</para>
/// </remarks>
public void lua_pcall()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pop">lua_pop</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pop
/// 		void lua_pop (lua_State *L, int n);
/// 		
/// 		从堆栈中弹出 n 个元素。
/// 		
/// 	</para>
/// </remarks>
public void lua_pop()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushboolean">lua_pushboolean</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushboolean
/// 		void lua_pushboolean (lua_State *L, int b);
/// 		
/// 		把 b 作为一个 boolean 值压入堆栈。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushboolean()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushcclosure">lua_pushcclosure</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushcclosure
/// 		void lua_pushcclosure (lua_State *L, lua_CFunction fn, int n);
/// 		
/// 		把一个新的 C closure 压入堆栈。
/// 		
/// 		当创建了一个 C 函数后，你可以给它关联一些值，这样就是在创建一个 C closure
/// 		（参见 §3.4）；
/// 		接下来无论函数何时被调用，这些值都可以被这个函数访问到。
/// 		为了将一些值关联到一个 C 函数上，
/// 		首先这些值需要先被压入堆栈（如果有多个值，第一个先压）。
/// 		接下来调用 lua_pushcclosure
/// 		来创建出 closure 并把这个 C 函数压到堆栈上。
/// 		参数 n 告之函数有多少个值需要关联到函数上。
/// 		lua_pushcclosure 也会把这些值从栈上弹出。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushcclosure()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushcfunction">lua_pushcfunction</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushcfunction
/// 		void lua_pushcfunction (lua_State *L, lua_CFunction f);
/// 		
/// 		将一个 C 函数压入堆栈。
/// 		这个函数接收一个 C 函数指针，并将一个类型为 function 的 Lua 值
/// 		压入堆栈。当这个栈顶的值被调用时，将触发对应的 C 函数。
/// 		
/// 		注册到 Lua 中的任何函数都必须遵循正确的协议来接收参数和返回值
/// 		（参见 lua_CFunction）。
/// 		
/// 		lua_pushcfunction 是作为一个宏定义出现的：
/// 		
/// 		     #define lua_pushcfunction(L,f)  lua_pushcclosure(L,f,0)
/// 		
/// 	</para>
/// </remarks>
public void lua_pushcfunction()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushfstring">lua_pushfstring</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushfstring
/// 		const char *lua_pushfstring (lua_State *L, const char *fmt, ...);
/// 		
/// 		把一个格式化过的字符串压入堆栈，然后返回这个字符串的指针。
/// 		它和 C 函数 sprintf 比较像，不过有一些重要的区别：
/// 		
/// 		• 
/// 		摸你需要为结果分配空间：
/// 		其结果是一个 Lua 字符串，由 Lua 来关心其内存分配
/// 		（同时通过垃圾收集来释放内存）。
/// 		
/// 		• 
/// 		这个转换非常的受限。
/// 		不支持 flag ，宽度，或是指定精度。
/// 		它只支持下面这些：
/// 		'%%' （插入一个 '%'），
/// 		'%s' （插入一个带零终止符的字符串，没有长度限制），
/// 		'%f' （插入一个 lua_Number），
/// 		'%p' （插入一个指针或是一个十六进制数），
/// 		'%d' （插入一个 int)，
/// 		'%c' （把一个 int 作为一个字符插入）。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushfstring()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushinteger">lua_pushinteger</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushinteger
/// 		void lua_pushinteger (lua_State *L, lua_Integer n);
/// 		
/// 		把 n 作为一个数字压栈。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushinteger()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushlightuserdata">lua_pushlightuserdata</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushlightuserdata
/// 		void lua_pushlightuserdata (lua_State *L, void *p);
/// 		
/// 		把一个 light userdata 压栈。
/// 		
/// 		userdata 在 Lua 中表示一个 C 值。
/// 		light userdata 表示一个指针。
/// 		它是一个像数字一样的值：
/// 		你不需要专门创建它，它也没有独立的 metatable ，
/// 		而且也不会被收集（因为从来不需要创建）。
/// 		只要表示的 C 地址相同，两个 light userdata 就相等。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushlightuserdata()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushlstring">lua_pushlstring</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushlstring
/// 		void lua_pushlstring (lua_State *L, const char *s, size_t len);
/// 		
/// 		把指针 s 指向的长度为 len 的字符串压栈。
/// 		Lua 对这个字符串做一次内存拷贝（或是复用一个拷贝），
/// 		因此 s 处的内存在函数返回后，可以释放掉或是重用于其它用途。
/// 		字符串内可以保存有零字符。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushlstring()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushnil">lua_pushnil</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushnil
/// 		void lua_pushnil (lua_State *L);
/// 		
/// 		把一个 nil 压栈。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushnil()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushnumber">lua_pushnumber</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushnumber
/// 		void lua_pushnumber (lua_State *L, lua_Number n);
/// 		
/// 		把一个数字 n 压栈。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushnumber()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushstring">lua_pushstring</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushstring
/// 		void lua_pushstring (lua_State *L, const char *s);
/// 		
/// 		把指针 s 指向的以零结尾的字符串压栈。
/// 		Lua 对这个字符串做一次内存拷贝（或是复用一个拷贝），
/// 		因此 s 处的内存在函数返回后，可以释放掉或是重用于其它用途。
/// 		字符串中不能包含有零字符；第一个碰到的零字符会认为是字符串的结束。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushstring()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushthread">lua_pushthread</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushthread
/// 		int lua_pushthread (lua_State *L);
/// 		
/// 		把 L 中提供的线程压栈。
/// 		如果这个线程是当前状态机的主线程的话，返回 1 。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushthread()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushvalue">lua_pushvalue</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushvalue
/// 		void lua_pushvalue (lua_State *L, int index);
/// 		
/// 		把堆栈上给定有效处索引处的元素作一个拷贝压栈。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushvalue()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_pushvfstring">lua_pushvfstring</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_pushvfstring
/// 		const char *lua_pushvfstring (lua_State *L,
/// 		                              const char *fmt,
/// 		                              va_list argp);
/// 		
/// 		等价于 lua_pushfstring，
/// 		不过是用 va_list 接收参数，而不是用可变数量的实际参数。
/// 		
/// 	</para>
/// </remarks>
public void lua_pushvfstring()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_rawequal">lua_rawequal</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_rawequal
/// 		int lua_rawequal (lua_State *L, int index1, int index2);
/// 		
/// 		如果两个索引 index1 和 index2 处的值简单地相等
/// 		（不调用元方法）则返回 1 。
/// 		否则返回 0 。
/// 		如果任何一个索引无效也返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_rawequal()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_rawget">lua_rawget</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_rawget
/// 		void lua_rawget (lua_State *L, int index);
/// 		
/// 		类似于 lua_gettable，
/// 		但是作一次直接访问（不触发元方法）。
/// 		
/// 	</para>
/// </remarks>
public void lua_rawget()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_rawgeti">lua_rawgeti</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_rawgeti
/// 		void lua_rawgeti (lua_State *L, int index, int n);
/// 		
/// 		把 t[n] 的值压栈，
/// 		这里的 t 是指给定索引 index 处的一个值。
/// 		这是一个直接访问；就是说，它不会触发元方法。
/// 		
/// 	</para>
/// </remarks>
public void lua_rawgeti()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_rawset">lua_rawset</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_rawset
/// 		void lua_rawset (lua_State *L, int index);
/// 		
/// 		类似于 lua_settable，
/// 		但是是作一个直接赋值（不触发元方法）。
/// 		
/// 	</para>
/// </remarks>
public void lua_rawset()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_rawseti">lua_rawseti</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_rawseti
/// 		void lua_rawseti (lua_State *L, int index, int n);
/// 		
/// 		等价于 t[n] = v，
/// 		这里的 t 是指给定索引 index 处的一个值，
/// 		而 v 是栈顶的值。
/// 		
/// 		函数将把这个值弹出栈。
/// 		赋值操作是直接的；就是说，不会触发元方法。
/// 		
/// 	</para>
/// </remarks>
public void lua_rawseti()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_Reader">lua_Reader</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_Reader
/// 		typedef const char * (*lua_Reader) (lua_State *L,
/// 		                                    void *data,
/// 		                                    size_t *size);
/// 		
/// 		lua_load 用到的读取器函数，
/// 		每次它需要一块新的 chunk 的时候，
/// 		lua_load 就调用读取器，
/// 		每次都会传入一个参数 data 。
/// 		读取器需要返回含有新的 chunk 的一块内存的指针，
/// 		并把 size 设为这块内存的大小。
/// 		内存块必须在下一次函数被调用之前一直存在。
/// 		读取器可以通过返回一个 NULL 来指示 chunk 结束。
/// 		读取器可能返回多个块，每个块可以有任意的大于零的尺寸。
/// 		
/// 	</para>
/// </remarks>
public void lua_Reader()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_register">lua_register</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_register
/// 		void lua_register (lua_State *L,
/// 		                   const char *name,
/// 		                   lua_CFunction f);
/// 		
/// 		把 C 函数 f 设到全局变量 name 中。
/// 		它通过一个宏定义：
/// 		
/// 		     #define lua_register(L,n,f) \
/// 		            (lua_pushcfunction(L, f), lua_setglobal(L, n))
/// 		
/// 	</para>
/// </remarks>
public void lua_register()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_remove">lua_remove</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_remove
/// 		void lua_remove (lua_State *L, int index);
/// 		
/// 		从给定有效索引处移除一个元素，
/// 		把这个索引之上的所有元素移下来填补上这个空隙。
/// 		不能用伪索引来调用这个函数，
/// 		因为伪索引并不指向真实的栈上的位置。
/// 		
/// 	</para>
/// </remarks>
public void lua_remove()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_replace">lua_replace</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_replace
/// 		void lua_replace (lua_State *L, int index);
/// 		
/// 		把栈顶元素移动到给定位置（并且把这个栈顶元素弹出），
/// 		不移动任何元素（因此在那个位置处的值被覆盖掉）。
/// 		
/// 	</para>
/// </remarks>
public void lua_replace()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_resume">lua_resume</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_resume
/// 		int lua_resume (lua_State *L, int narg);
/// 		
/// 		在给定线程中启动或继续一个 coroutine 。
/// 		
/// 		要启动一个 coroutine 的话，首先你要创建一个新线程
/// 		（参见 lua_newthread ）；
/// 		然后把主函数和若干参数压到新线程的堆栈上；
/// 		最后调用 lua_resume ，
/// 		把 narg 设为参数的个数。
/// 		这次调用会在 coroutine 挂起时或是结束运行后返回。
/// 		当函数返回时，堆栈中会有传给 lua_yield 的所有值，
/// 		或是主函数的所有返回值。
/// 		如果 coroutine 切换时，lua_resume 返回
/// 		LUA_YIELD ，
/// 		而当 coroutine 结束运行且没有任何错误时，返回 0 。
/// 		如果有错则返回错误代码（参见 lua_pcall）。
/// 		在发生错误的情况下，
/// 		堆栈没有展开，
/// 		因此你可以使用 debug API 来处理它。
/// 		出错信息放在栈顶。
/// 		要继续运行一个 coroutine 的话，你把需要传给 yield
/// 		作结果的返回值压入堆栈，然后调用 lua_resume 。
/// 		
/// 	</para>
/// </remarks>
public void lua_resume()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_setallocf">lua_setallocf</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_setallocf
/// 		void lua_setallocf (lua_State *L, lua_Alloc f, void *ud);
/// 		
/// 		把指定状态机的分配器函数换成带上指针 ud 的 f 。
/// 		
/// 	</para>
/// </remarks>
public void lua_setallocf()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_setfenv">lua_setfenv</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_setfenv
/// 		int lua_setfenv (lua_State *L, int index);
/// 		
/// 		从堆栈上弹出一个 table 并把它设为指定索引处值的新环境。
/// 		如果指定索引处的值即不是函数又不是线程或是 userdata ，
/// 		lua_setfenv 会返回 0 ，
/// 		否则返回 1 。
/// 		
/// 	</para>
/// </remarks>
public void lua_setfenv()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_setfield">lua_setfield</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_setfield
/// 		void lua_setfield (lua_State *L, int index, const char *k);
/// 		
/// 		做一个等价于 t[k] = v 的操作，
/// 		这里 t 是给出的有效索引 index 处的值，
/// 		而 v 是栈顶的那个值。
/// 		
/// 		这个函数将把这个值弹出堆栈。
/// 		跟在 Lua 中一样，这个函数可能触发一个 "newindex" 事件的元方法
/// 		（参见 §2.8）。
/// 		
/// 	</para>
/// </remarks>
public void lua_setfield()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_setglobal">lua_setglobal</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_setglobal
/// 		void lua_setglobal (lua_State *L, const char *name);
/// 		
/// 		从堆栈上弹出一个值，并将其设到全局变量 name 中。
/// 		它由一个宏定义出来：
/// 		
/// 		     #define lua_setglobal(L,s)   lua_setfield(L, LUA_GLOBALSINDEX, s)
/// 		
/// 	</para>
/// </remarks>
public void lua_setglobal()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_setmetatable">lua_setmetatable</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_setmetatable
/// 		int lua_setmetatable (lua_State *L, int index);
/// 		
/// 		把一个 table 弹出堆栈，并将其设为给定索引处的值的 metatable 。
/// 		
/// 	</para>
/// </remarks>
public void lua_setmetatable()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_settable">lua_settable</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_settable
/// 		void lua_settable (lua_State *L, int index);
/// 		
/// 		作一个等价于 t[k] = v 的操作，
/// 		这里 t 是一个给定有效索引 index 处的值，
/// 		v 指栈顶的值，
/// 		而 k 是栈顶之下的那个值。
/// 		
/// 		这个函数会把键和值都从堆栈中弹出。
/// 		和在 Lua 中一样，这个函数可能触发 "newindex" 事件的元方法
/// 		（参见 §2.8）。
/// 		
/// 	</para>
/// </remarks>
public void lua_settable()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_settop">lua_settop</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_settop
/// 		void lua_settop (lua_State *L, int index);
/// 		
/// 		参数允许传入任何可接受的索引以及 0 。
/// 		它将把堆栈的栈顶设为这个索引。
/// 		如果新的栈顶比原来的大，超出部分的新元素将被填为 nil 。
/// 		如果 index 为 0 ，把栈上所有元素移除。
/// 		
/// 	</para>
/// </remarks>
public void lua_settop()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_State">lua_State</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_State
/// 		typedef struct lua_State lua_State;
/// 		
/// 		一个不透明的结构，它保存了整个 Lua 解释器的状态。
/// 		Lua 库是完全可重入的：
/// 		它没有任何全局变量。
/// 		（译注：从 C 语法上来说，也不尽然。例如，在 table 的实现中
/// 		用了一个静态全局变量 dummynode_ ，但这在正确使用时并不影响可重入性。
/// 		只是万一你错误链接了 lua 库，不小心在同一进程空间中存在两份 lua 库实现的代码的话，
/// 		多份 dummynode_ 不同的地址会导致一些问题。）
/// 		所有的信息都保存在这个结构中。
/// 		
/// 		这个状态机的指针必须作为第一个参数传递给每一个库函数。
/// 		lua_newstate 是一个例外，
/// 		这个函数会从头创建一个 Lua 状态机。
/// 		
/// 	</para>
/// </remarks>
public void lua_State()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_status">lua_status</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_status
/// 		int lua_status (lua_State *L);
/// 		
/// 		返回线程 L 的状态。
/// 		
/// 		正常的线程状态是 0 。
/// 		当线程执行完毕或发生一个错误时，状态值是错误码。
/// 		如果线程被挂起，状态为 LUA_YIELD 。
/// 		
/// 	</para>
/// </remarks>
public void lua_status()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_toboolean">lua_toboolean</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_toboolean
/// 		int lua_toboolean (lua_State *L, int index);
/// 		
/// 		把指定的索引处的的 Lua 值转换为一个 C 中的 boolean 值（ 0 或是 1 ）。
/// 		和 Lua 中做的所有测试一样，
/// 		lua_toboolean 会把任何
/// 		不同于 false 和 nil 的值当作 1 返回；
/// 		否则就返回 0 。
/// 		如果用一个无效索引去调用也会返回 0 。
/// 		（如果你想只接收真正的 boolean 值，就需要使用
/// 		lua_isboolean 来测试值的类型。）
/// 		
/// 	</para>
/// </remarks>
public void lua_toboolean()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_tocfunction">lua_tocfunction</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_tocfunction
/// 		lua_CFunction lua_tocfunction (lua_State *L, int index);
/// 		
/// 		把给定索引处的 Lua 值转换为一个 C 函数。
/// 		这个值必须是一个 C 函数；如果不是就返回
/// 		NULL 。
/// 		
/// 	</para>
/// </remarks>
public void lua_tocfunction()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_tointeger">lua_tointeger</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_tointeger
/// 		lua_Integer lua_tointeger (lua_State *L, int idx);
/// 		
/// 		把给定索引处的 Lua 值转换为 lua_Integer 
/// 		这样一个有符号整数类型。
/// 		这个 Lua 值必须是一个数字或是一个可以转换为数字的字符串
/// 		（参见 §2.2.1）；
/// 		否则，lua_tointeger 返回 0 。
/// 		
/// 		如果数字不是一个整数，
/// 		截断小数部分的方式没有被明确定义。
/// 		
/// 	</para>
/// </remarks>
public void lua_tointeger()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_tolstring">lua_tolstring</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_tolstring
/// 		const char *lua_tolstring (lua_State *L, int index, size_t *len);
/// 		
/// 		把给定索引处的 Lua 值转换为一个 C 字符串。
/// 		如果 len 不为 NULL ，
/// 		它还把字符串长度设到 *len 中。
/// 		这个 Lua 值必须是一个字符串或是一个数字；
/// 		否则返回返回 NULL 。
/// 		如果值是一个数字，lua_tolstring 
/// 		还会把堆栈中的那个值的实际类型转换为一个字符串。
/// 		（当遍历一个表的时候，把 lua_tolstring
/// 		作用在键上，这个转换有可能导致 lua_next 弄错。）
/// 		
/// 		lua_tolstring 返回 Lua 状态机中
/// 		字符串的以对齐指针。
/// 		这个字符串总能保证 （ C 要求的）最后一个字符为零 ('\0') ，
/// 		而且它允许在字符串内包含多个这样的零。
/// 		因为 Lua 中可能发生垃圾收集，
/// 		所以不保证 lua_tolstring 返回的指针，
/// 		在对应的值从堆栈中移除后依然有效。
/// 		
/// 	</para>
/// </remarks>
public void lua_tolstring()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_tonumber">lua_tonumber</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_tonumber
/// 		lua_Number lua_tonumber (lua_State *L, int index);
/// 		
/// 		把给定索引处的 Lua 值转换为 lua_Number
/// 		这样一个 C 类型（参见 lua_Number ）。
/// 		这个 Lua 值必须是一个数字或是一个可转换为数字的字符串
/// 		（参见 §2.2.1 ）；
/// 		否则，lua_tonumber 返回 0 。
/// 		
/// 	</para>
/// </remarks>
public void lua_tonumber()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_topointer">lua_topointer</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_topointer
/// 		const void *lua_topointer (lua_State *L, int index);
/// 		
/// 		把给定索引处的值转换为一般的 C 指针 (void*) 。
/// 		这个值可以是一个 userdata ，table ，thread 或是一个 function ；
/// 		否则，lua_topointer 返回 NULL 。
/// 		不同的对象有不同的指针。
/// 		不存在把指针再转回原有类型的方法。
/// 		
/// 		这个函数通常只为产生 debug 信息用。
/// 		
/// 	</para>
/// </remarks>
public void lua_topointer()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_tostring">lua_tostring</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_tostring
/// 		const char *lua_tostring (lua_State *L, int index);
/// 		
/// 		等价于 lua_tolstring ，而参数 len 设为 NULL 。
/// 		
/// 	</para>
/// </remarks>
public void lua_tostring()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_tothread">lua_tothread</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_tothread
/// 		lua_State *lua_tothread (lua_State *L, int index);
/// 		
/// 		把给定索引处的值转换为一个 Lua 线程（由 lua_State* 代表）。
/// 		这个值必须是一个线程；否则函数返回 NULL 。
/// 		
/// 	</para>
/// </remarks>
public void lua_tothread()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_touserdata">lua_touserdata</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_touserdata
/// 		void *lua_touserdata (lua_State *L, int index);
/// 		
/// 		如果给定索引处的值是一个完整的 userdata ，函数返回内存块的地址。
/// 		如果值是一个 light userdata ，那么就返回它表示的指针。
/// 		否则，返回 NULL 。
/// 		
/// 	</para>
/// </remarks>
public void lua_touserdata()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_type">lua_type</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_type
/// 		int lua_type (lua_State *L, int index);
/// 		
/// 		返回给定索引处的值的类型，
/// 		当索引无效时则返回 LUA_TNONE
/// 		（那是指一个指向堆栈上的空位置的索引）。
/// 		lua_type 返回的类型是一些个在 lua.h 中定义的常量：
/// 		LUA_TNIL ，
/// 		LUA_TNUMBER ，
/// 		LUA_TBOOLEAN ，
/// 		LUA_TSTRING ，
/// 		LUA_TTABLE ，
/// 		LUA_TFUNCTION ，
/// 		LUA_TUSERDATA ，
/// 		LUA_TTHREAD ，
/// 		LUA_TLIGHTUSERDATA 。
/// 		
/// 	</para>
/// </remarks>
public void lua_type()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_typename">lua_typename</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_typename
/// 		const char *lua_typename  (lua_State *L, int tp);
/// 		
/// 		返回 tp 表示的类型名，
/// 		这个 tp 必须是 lua_type 可能返回的值中之一。
/// 		
/// 	</para>
/// </remarks>
public void lua_typename()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_Writer">lua_Writer</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_Writer
/// 		typedef int (*lua_Writer) (lua_State *L,
/// 		                           const void* p,
/// 		                           size_t sz,
/// 		                           void* ud);
/// 		
/// 		由 lua_dump 用到的写入器函数。
/// 		每次 lua_dump 产生了一块新的 chunk ，它都会调用写入器。
/// 		传入要写入的缓存 (p) 和它的尺寸 (sz) ，
/// 		还有 lua_dump 的参数 data 。
/// 		
/// 		写入器会返回一个错误码：
/// 		0 表示没有错误；
/// 		别的值均表示一个错误，并且会让 lua_dump 停止再次调用写入器。
/// 		
/// 	</para>
/// </remarks>
public void lua_Writer()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_xmove">lua_xmove</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_xmove
/// 		void lua_xmove (lua_State *from, lua_State *to, int n);
/// 		
/// 		传递 同一个 全局状态机下不同线程中的值。
/// 		
/// 		这个函数会从 from 的堆栈中弹出 n 个值，
/// 		然后把它们压入 to 的堆栈中。
/// 		
/// 	</para>
/// </remarks>
public void lua_xmove()
{
}

/// <summary>
/// 	<see href="https://www.lua.org/manual/5.1/manual.html#lua_yield">lua_yield</see>
/// </summary>
/// <remarks>
/// 	<para>
/// 		lua_yield
/// 		int lua_yield  (lua_State *L, int nresults);
/// 		
/// 		切出一个 coroutine 。
/// 		
/// 		这个函数只能在一个 C 函数的返回表达式中调用。如下：
/// 		
/// 		     return lua_yield (L, nresults);
/// 		
/// 		当一个 C 函数这样调用 lua_yield ，
/// 		正在运行中的 coroutine 将从运行中挂起，
/// 		然后启动这个 coroutine 用的那次对 lua_resume 的调用就返回了。
/// 		参数 nresults 指的是堆栈中需要返回的结果个数，这些返回值将被传递给
/// 		lua_resume 。/// 	</para>
/// </remarks>
public void lua_yield()
{
}

