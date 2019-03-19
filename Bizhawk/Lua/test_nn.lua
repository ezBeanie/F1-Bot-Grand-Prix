local frames = 0
local host = "127.0.0.1"
local port = 8000

function split(s, delimiter)
    result = {};
    for match in (s .. delimiter):gmatch("(.-)" .. delimiter) do
        table.insert(result, match);
    end
    return result;
end

function setInputs(inputs)
    local current = {}
    current["A"] = inputs[1]
    current["B"] = inputs[2]
    current["X Axis"] = tostring(tonumber(inputs[3]) * 256 - 128)
    --current["Y Axis"] = tostring(tonumber(inputs[4]) * 256 - 128)
    joypad.set(current, 1)
    joypad.setanalog(current, 1)
    --console.log(joypad.get(1))
    --console.log(tonumber(inputs[3]) * 256 - 128)
end

while true do
    emu.frameadvance()
    --if frames % 2 == 0 then
    --console.log(getControls())
    inputs = split(comm.httpGet("http://" .. host .. ":" .. port), "x")
    console.log(inputs[3])
    console.log(tonumber(inputs[3]) * 256 - 128)
    setInputs(inputs)
    --console.log(comm.httpTest())
    --end
    frames = frames + 1
end