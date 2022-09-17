from datetime import datetime
import serial, sys, codecs
ser = serial.Serial("/dev/tty.usbserial-AB0N4H0H", 1200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
print(" ".join(sys.argv[1:]) + " - " + "{:%B %d, %Y %H:%M:%S}".format(datetime.now()))
run = 0
mmask = 0
aambient = 0
mmask_tot = 0
aambient_tot = 0
high_pct = 0
low_pct = 99.9999999
first = ""
start = datetime.now()
while True:
    line = ser.readline().decode("utf-8")
    words = line.split()
    if words[0] == "Mask":
        mmask = float(words[1])
        aambient = 0
    if words[0] == "Ambient":
        aambient = float(words[1])
    if mmask > 0 and aambient > 0:
        pct = ((aambient - mmask) / aambient) * 100
        if pct > high_pct:
            high_pct = pct
        if pct < low_pct:
            low_pct = pct
        mmask_tot = mmask_tot + mmask
        aambient_tot = aambient_tot + aambient
        pct_ave = ((aambient_tot - mmask_tot) / aambient_tot) * 100
        run = run + 1
        sys.stdout.write("Run " + str(run) + ": " + str("%.4f" % pct) + "%, ave so far: " + str("%.4f" % pct_ave) + "%\n")
        mmask = 0
        aambient = 0
    if words[0] == "Overall":
        pct_ave = ((aambient_tot - mmask_tot) / aambient_tot) * 100
        sys.stdout.write("Overall Average: " + str("%.4f" % pct_ave) + "%\n")
        sys.stdout.write("High: " + str("%.4f" % high_pct) + "%\n")
        sys.stdout.write("Low: " + str("%.4f" % low_pct) + "%\n")
        sys.stdout.write("Duration: {:.2f} mins\n".format((datetime.now() - start).total_seconds() / 60))
        exit(0)
    if words[0] == "Ave." and words[1] == "Conc.":
        if first == "":
            first = datetime.now()
            print("ts, duration mins, test, count")
        print(datetime.now().isoformat() + ", " + "{:.2f}".format((datetime.now() - first).total_seconds() / 60) + ", \"" + " ".join(sys.argv[1:]) + "\", " + words[2])
    # sys.stdout.write("-- line " + line + "--" + str(len(words)))
