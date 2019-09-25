#!../lua

math.randomseed(0)

collectgarbage("setstepmul", 180)
collectgarbage("setpause", 190)


--[=[
  example of a long [comment],
  [[spanning several [lines]]]

]=]

print("current path:\n  " .. string.gsub(package.path, ";", "\n  "))


local msgs = {}
function Message (m)
  print(m)
  msgs[#msgs+1] = string.sub(m, 3, -3)
end


local c = os.clock()

assert(os.setlocale"C")

local T,print,gcinfo,format,write,assert,type =
      T,print,gcinfo,string.format,io.write,assert,type

local function formatmem (m)
  if m < 1024 then return m
  else
    m = m/1024 - m/1024%1
    if m < 1024 then return m.."K"
    else
      m = m/1024 - m/1024%1
      return m.."M"
    end
  end
end

local showmem = function ()
  if not T then
    print(format("    ---- total memory: %s ----\n", formatmem(gcinfo())))
  else
    T.checkmemory()
    local a,b,c = T.totalmem()
    local d,e = gcinfo()
    print(format(
  "\n    ---- total memory: %s (%dK), max use: %s,  blocks: %d\n",
                        formatmem(a),  d,      formatmem(c),           b))
  end
end


--
-- redefine dofile to run files through dump/undump
--
dofile = function (n)
  showmem()
  local f = assert(loadfile(n))
  local b = string.dump(f)
  f = assert(loadstring(b))
  return f()
end

dofile('main.file')

do
  local u = newproxy(true)
  local newproxy, stderr = newproxy, io.stderr
  getmetatable(u).__gc = function (o)
    stderr:write'.'
    newproxy(o)
  end
end

local f = assert(loadfile('gc.file'))
f()
dofile('db.file')
assert(dofile('calls.file') == deep and deep)
dofile('strings.file')
dofile('literals.file')
assert(dofile('attrib.file') == 27)
assert(dofile('locals.file') == 5)
dofile('constructs.file')
dofile('code.file')
do
  local f = coroutine.wrap(assert(loadfile('big.file')))
  assert(f() == 'b')
  assert(f() == 'a')
end
dofile('nextvar.file')
dofile('pm.file')
dofile('api.file')
assert(dofile('events.file') == 12)
dofile('vararg.file')
dofile('closure.file')
dofile('errors.file')
dofile('math.file')
dofile('sort.file')
assert(dofile('verybig.file') == 10); collectgarbage()
dofile('files.file')

if #msgs > 0 then
  print("\ntests not performed:")
  for i=1,#msgs do
    print(msgs[i])
  end
  print()
end

print("final OK !!!")
print('cleaning all!!!!')

debug.sethook(function (a) assert(type(a) == 'string') end, "cr")

local _G, collectgarbage, showmem, print, format, clock =
      _G, collectgarbage, showmem, print, format, os.clock

local a={}
for n in pairs(_G) do a[n] = 1 end
a.tostring = nil
a.___Glob = nil
for n in pairs(a) do _G[n] = nil end

a = nil
collectgarbage()
collectgarbage()
collectgarbage()
collectgarbage()
collectgarbage()
collectgarbage();showmem()

print(format("\n\ntotal time: %.2f\n", clock()-c))
