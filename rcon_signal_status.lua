hook.Add("PlayerSay", "RCON_SignalStatus", function(ply, text)
    if not string.StartWith(text, "!sigstate") then return end

    local args = string.Explode(" ", text)
    if not args[2] then
        print("[SIGSTATE] Ошибка: имя сигнала не указано")
        return ""
    end

    local signalName = string.lower(args[2])
    local signal = Metrostroi.GetSignalByName(signalName)

    if not IsValid(signal) then
        print("[SIGSTATE] Сигнал " .. signalName .. " не найден")
        return ""
    end

    local aspect = signal:GetAspect() or "неизвестно"

    -- Таблица расшифровки аспектов
    local aspectText = {
        R = "красный",
        Y = "жёлтый",
        G = "зелёный",
        BY = "бело-жёлтый",
        B = "белый",
        YY = "двойной жёлтый",
        GY = "зелёный-жёлтый",
        RG = "красно-зелёный",
        [""] = "нет сигнала"
    }

    local humanReadable = aspectText[aspect] or aspect

    print("[SIGSTATE] " .. signalName .. " = " .. humanReadable)
    return ""
end)
