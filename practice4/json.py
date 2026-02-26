import json

with open(r"C:\Users\kazir\Downloads\sample-data.json") as f:
    data=json.load(f)



print("Interface Status")
print("="*80)
print(f"{'DN':50} {'Description':20} {'Speed':6} {'MTU':6}")
print("-------------------------------------------------- --------------------  ------  ------")

first_int= data["imdata"][0]["l1PhysIf"]["attributes"]

dn=first_int["dn"]
descr=first_int["descr"]
speed=first_int["speed"]
mtu=first_int["mtu"]
print(f"{dn:50} {descr:20} {speed:6} {mtu:6}")

sec_int=data["imdata"][1]["l1PhysIf"]["attributes"]
dn1=sec_int["dn"]
descr1=sec_int["descr"]
speed1=sec_int["speed"]
mtu1=sec_int["mtu"]
print(f"{dn1:50} {descr1:20} {speed1:6} {mtu1:6}")

third_int=data["imdata"][2]["l1PhysIf"]["attributes"]

dn2=third_int["dn"]
descr2=third_int["descr"]
speed2=third_int["speed"]
mtu2=third_int["mtu"]

print(f"{dn2:50} {descr2:20} {speed2:6} {mtu2:6}")
