# Name : Angela Amani
# Date : 12/02/2026
# String_formatting

#Get string length
sentence = "I watch anime"

string_length = len(sentence)

print(f"The length is: {string_length}")

# Splitting a string
sentence_2 = "Mathematics Physics"
split = sentence_2.split(" ")

print(f"the first subject is: ", split[0])


# Make everythinG CAP 
mpesa_code = "ub21ddsfhg"

capitalized = mpesa_code.upper()

print("New mpesa code: ",capitalized)


mpesa_code = "AD34FGHDVN"

capitalized = mpesa_code.lower()

print("New mpesa code: ",capitalized)

balance = "100Kes"
amount_added = "50Kes"

cleaned_balance = balance.replace("Kes","")

print("cleaned_amount:", cleaned_balance)

cleaned_amount_added = amount_added.replace("Kes","")

print("cleaned amount added: ", cleaned_amount_added)

new_balance = int(cleaned_balance) + int(cleaned_amount_added)

print(f"The new balance is:", new_balance)

money = " 40Kes"
message = " CONFIRMED you have received "
sender = " from Philip" 

print(mpesa_code + message + money + sender)

 
added = "12.02Kes"
new_added = added.replace("Kes","")
print(f"New money is:{new_added}")
print(added)
print(money)
new_money = money.replace("Kes","")
print(f"New money :{new_money}")
print(new_added)
print(float(new_money))
results = (float(new_money)) + (float(new_added))
print(results)
new_results = round(results, 2)
print(new_results)
print(mpesa_code + message + str(new_results) + sender)
























