from analyzer import analyze

cases = [
    "Hôm nay tôi rất vui",
    "Buồn quá...",
    "Mk ko biết nữa",
    "Tệ vl",
    "Tuyệt vời luôn!",
    "Ok"
]

for c in cases:
    print(c, "→", analyze(c))
