from eth_account import Account
from eth_account.messages import encode_defunct

acct = Account.create()  # TUYỆT ĐỐI không dùng khóa này cho tiền thật
print("address:", acct.address)
msg = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 3")
sig1 = Account.sign_message(msg, acct.key)
sig2 = Account.sign_message(msg, acct.key)
print("sig1 r,s,v:", hex(sig1.r), hex(sig1.s), sig1.v)
print("sig2 r,s,v:", hex(sig2.r), hex(sig2.s), sig2.v)
print("giống hệt nhau?", sig1.signature == sig2.signature)
who = Account.recover_message(msg, signature=sig1.signature)
print("recovered:", who, "| match:", who == acct.address)

bad = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 4")
who_bad = Account.recover_message(bad, signature=sig1.signature)
print("tampered ->", who_bad)