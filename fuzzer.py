import requests


for uid in USER_IDS:
test_url = f"{endpoint}/{uid}"
try:
headers = {}
if token:
headers["Authorization"] = f"Bearer {token}"


response = requests.get(test_url, headers=headers)


if response.status_code == 200:
idor_results.append({
"potential_idor": True,
"url": test_url,
"response": response.text[:200]
})


except Exception as e:
idor_results.append({"error": str(e)})


return idor_results




def main():
parser = argparse.ArgumentParser()
parser.add_argument("--endpoints", required=True, help="File with endpoint URLs")
parser.add_argument("--token", help="Optional Bearer token")
args = parser.parse_args()


with open(args.endpoints, "r") as f:
endpoints = [line.strip() for line in f.readlines()]


final_report = []


for ep in endpoints:
print(f"[+] Fuzzing: {ep}")
fuzz_results = fuzz_endpoint(ep, args.token)
idor_results = check_idor(ep, args.token)


final_report.append({
"endpoint": ep,
"fuzz_results": fuzz_results,
"idor_results": idor_results
})


with open("report.json", "w") as out:
json.dump(final_report, out, indent=4)


print("\n[✓] Fuzzing completed. Results saved to report.json")




if __name__ == "__main__":
main()
