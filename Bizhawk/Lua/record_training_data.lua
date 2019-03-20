local frames = 0
local host = "127.0.0.1"
local port = 8000

function getAnalogControls()
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
    controls = controls .. (allControls["X Axis"] + 128) / 128
    return controls
end

function getDiscreteControls()
    controls = ""
    allControls = joypad.get(1)
    if allControls["A"] then
        controls = controls .. "1"
    else
        controls = controls .. "0"
    end
    if allControls["B"] then
        controls = controls .. "x1"
    else
        controls = controls .. "x0"
    end
    if allControls["A Left"] then
        controls = controls .. "x1"
    else
        controls = controls .. "x0"
    end
    if allControls["A Right"] then
        controls = controls .. "x1"
    else
        controls = controls .. "x0"
    end
    return controls
end

while true do
    emu.frameadvance()
    if frames % 2 == 0 then
        --console.log(getAnalogControls())
        --console.log(joypad.get(1))
        comm.httpPost("http://" .. host .. ":" .. port, getAnalogControls())
        --console.log(comm.httpTest())
    end
    frames = frames + 1
end