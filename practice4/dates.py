from datetime import date, timedelta
cur=date.today()
newd=cur-timedelta(days=5)

print(f"Current day:{cur}")
print(f"5 days substracted:{newd}")


yesterday=cur-timedelta(days=1)
tomorrow=cur+timedelta(days=1)

print(f"Yesterday:{yesterday}")
print(f"Tomorrow:{tomorrow}")

print()
from datetime import datetime
abc=datetime.now()
print(abc)



print()
diff=tomorrow-yesterday
print(f"Difference:{diff}")
print(f"Difference in seconds:{diff.total_seconds()}")
