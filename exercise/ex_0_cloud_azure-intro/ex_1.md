## 1. Understand IaaS and PaaS with the Azure SQL family
In lecture 03_Azure_intro, we briefly mention that you can choose IaaS and PaaS options from the Azure SQL family to host relational data in Azure. <br>

Suppose you are a data engineer and would like to make a suggestion to your manager about which option to choose, can you intuitively explain to your manager what are the responsibilities you are shared with Azure for different options? 

Read through the reference below to help you formulate your suggestion: <br>

---
### Solutinon 

**IaaS**
- Du kontrollera: applikationen, data, operativ systemet, mjukvareprogram and runtime.
- Azure kontrollera: Server, Storage, networking och Virtualisering.

***PaaS***
- Du kontrollera: applikationen, data.
- Azure control: operativ systemet, mjukvareprogram, runtime, server, storage, networking och virtualiseringen.

***SaaS***
- Du kontrollera:  --
- Azure kontrollera: applikationen, data, operativ systemet, mjukvareprogram, runtime, server, storage, networking och virtualiseringen.

Så om du bara vill att cloud ska bara hantera hårdvaran men du vill ha kontroll på appliakionen, data, körtiden, opretiv systemet och mjukvareprogram så ska du välja Iass.
Men om du vill att bara ha hand om applikationen och data så ska du använda Paas. 
Sist om du bara vill connecta upp dig med cloud när du vill köra din applikation så kan du välja SaaS. Allt sköts i cloud då.