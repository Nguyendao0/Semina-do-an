from database import save_history, get_history

save_history("Hôm nay tôi vui", "POSITIVE")
save_history("Buồn quá", "NEGATIVE")

print(get_history())
