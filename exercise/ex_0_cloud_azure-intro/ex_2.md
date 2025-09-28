## 2. Create your first Window virtual machine
Follow [this video](https://www.youtube.com/watch?v=4TgwLKhLoCc) to create your first Window VM. For the VM size, choose *Standard D2s v3 (2 vcpus, 8 GiB memory)* instead. 

a) Can you explain how the configuration of Region and Availability Zone affect the uptime of your VM?

b) How many resources are created in your resource group when you create a VM? Can you guess what are they?

c) Explore the use of Bastion to connect to your VM. When the connection is successful, can you navigate within your VM and check your disk size?

>[!Warning]
>When you are done with question 2, remove the resource groups you have created to save credits!

----
## solution

a) 
- Rgioner: Vilket land/Stad min VM körs i.
Om man väljer rgioner långt bort desto längre tar datatrafiken och man får hög latency.
- Availability zone: vilket specifik datacenter i regionen. Uptime: Om man sprider resource i flera zoner, minskar man risken att ett enskilt fel tar ner din tjänst.


b) 6 stycken
- virtual machine: Kör själva operativ systemet och programmen. Innehåller CPU och RAM. Är själva datorn som man skapar i AZURE.
- ip: Ger VM en publik adress på internet. Utan den skulle VM bara vara tillgänglig på AZURE-nätverk
- nsg: Nätverk Security Group, en brandvägg för ditt nätverk, skyddar VM mot oönskad trafik. Bestämmer vilka portar som är öppna.
- VNET: Virtual Network, Ett privat nätverk i AZURE. VM placeras i subnet i detta nätvwerk. Gör så att resource kan prata med varandra utan att gå via internet.
- OS Disk: Managed Disk, VM:s systemdisk. Innehåller operativsystemet och filerna som man sparar.