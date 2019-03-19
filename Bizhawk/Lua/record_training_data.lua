local frames = 0
local host = "127.0.0.1"
local port = 8000

function getControls()
    controls = ""
    allControls = joypad.get(1)
    if allControls["A"] then
        controls = controls .. "1"
    else
        controls = controls .. "0"
    end
    if allControls["B"] then
        controls = controls .. "x1x"
    else
        controls = controls .. "x0x"
    end
    controls = controls .. (allControls["X Axis"] + 128) / 256 .. "x" .. (allControls["Y Axis"] + 128) / 256
    return controls
end

while true do
    emu.frameadvance()
    if frames % 2 == 0 then
        --console.log(getControls())
        comm.httpPost("http://" .. host .. ":" .. port, getControls())
        --console.log(comm.httpTest())
    end
    frames = frames + 1
end