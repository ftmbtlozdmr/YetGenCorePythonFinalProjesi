import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

#13 Mayıs 2023 Yetgen Seçimleri
class Voter:
    # Class yapısı, her bir oy veren kişiyi temsil ediyor.
    def __init__(self,yetgen_id,isim,soyisim,seçim,lider):
        self.yetgen_id = yetgen_id
        self.isim = isim
        self.soyisim = soyisim
        self.seçim = seçim
        self.lider = lider


    def __str__(self):
        return f"{self.yetgen_id},{self.isim},{self.soyisim},{self.lider}"

voters = []

""" Bu method kişnin yetgen mensubu olup olmadığını kontrol ediyor.  Eğer methodun aldığı input yetgingenvler.txt dosyasının içerisinde ise False döndürüyor. """
def valid_check(yetgen_id):

    try:
        file1 = open("YetkinGencler2.txt","r")
        Lines = file1.readlines()
    except FileNotFoundError:
        print(f"Error: dosya bulunamadı {file1}")
    except IOError as e:
        print(f"Error: {e}")

    for line in Lines:
        if int(yetgen_id) == int(line):
            return False
    return True


    """ Bu method kişinin daha önce oy verip vermediğini kontrol ediyor. Bunu ise voters listesisinin elemanlarına bakarak yapıyor. Eğer methodun aldığı input
bu listenin elemanlarının(Bu listenin elemanlarının hepsi birer object-Voter class'ı kullanılarak yaratılan- eğer eşleşme bulursa True döndürüyor, yoksa false döndürüyor) """
def multiple_check(yetgen_id):
    # Burada kişinin daha önce oy kullanıp kullanmadığı kontrol ediliyor.
    for voter in voters:
        if voter.yetgen_id == yetgen_id:
            return True
    return False
    # Aynı kısımda kişinin yetgen üyesi olup olmadığı kontrol edilebilir.


"""
def end_election():
Bu method aslında main method olarak düşünülebilir. Bir başka deyişle seçimi sonlandır butonuna basıldığında gerçekleşmesini istediğimiz olaylar.
1-Öncelikle voters listesinde bulunan tüm objeler str methodu(Class'ta yazılmış olan method) ile dosya içerisine yazılıyor.(Bilgileri sakladığımız kısım, dosya aslında başka bir işe yaramıyor.)
2-Daha sonra bir döngü içerinde lidere bağlı toplam oy sayılarını buluyor.
3- Javanın ve pythonun toplam aldığı oyları hesaplıyor.
4-Matplotlib ve hesaplana bilgileri kullanarak gerekli grafikleri ekrana yazdırıyor.
"""
def end_election():
    with open("oy_bilgileri","w") as f:
        for voter in voters:
            f.write(str(voter) + "\n")

    seçimler = ["Python İttifakı", "Java İttifakı"]
    liderler = ["Enes", "Mustafa", "Begüm", "Ahmet","Mertcan","Hakan","Metin","Mücahit"]
    lidere_göre_oy_sayilari = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]] # Bu kısım elbette lider sayısına göre güncellenecek

    for voter in voters:
        seçim = voter.seçim
        lider = voter.lider
        if seçim == "a":
            lidere_göre_oy_sayilari[liderler.index(lider)][0] += 1
        if seçim == "b":
            lidere_göre_oy_sayilari[liderler.index(lider)][1] += 1
    

    java_toplam = 0
    python_toplam = 0

    
    for i in range(len(lidere_göre_oy_sayilari)):
        # Oyların aday başına hesaplanması
        java_toplam += lidere_göre_oy_sayilari[i][1]
        python_toplam += lidere_göre_oy_sayilari[i][0]
       
    toplam_oy = len(voters)
    beklenen_oy = 25

    labels = ["Seçime Katılanlar", "Seçime Katılmayanlar"]
    sizes = [toplam_oy,beklenen_oy-toplam_oy]

    x_values = ["Python İttifakı","Java İttifakı"]
    y_values = [python_toplam,java_toplam]

    explode = [0,0.1]
    colors = [
        "#1bf54e",
        "#bf0808"
    ]

    fig, (axs1, ax2) = plt.subplots(1,2,figsize=(9,5))
    axs1.pie(sizes,explode=explode,colors=colors,autopct='%1.0f%%',startangle=90)
    axs1.legend(["Seçime Katılanlar","Seçime Katılmayanlar"],loc=3,fontsize=10)
    axs1.set_title("Seçime Katılım Oranı")

    ax2.bar(x_values,y_values,color=['#0c5a91', 'orange'])
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.set_title("Genel Oylama")


    fig, axs = plt.subplots(2,4, figsize=(16,8))
    for i in range(len(liderler)):
        row = i//4
        col = i%4
        axs[row,col].bar(seçimler, lidere_göre_oy_sayilari[i],color=['#0c5a91', 'orange'])
        axs[row,col].yaxis.set_major_locator(MaxNLocator(integer=True))
        axs[row,col].set_title(f"Lidere Göre Seçim Sonuçları ({liderler[i]})")
        axs[row,col].set_ylabel("Oy Sayıları") 
    plt.suptitle(f"Lidere Bağlı Seçim Sonuçları ( Toplam Oy: {toplam_oy})", fontsize = 16)
    plt.tight_layout()
    plt.show()

"""
oy_ver():
Bu method aslında oy ver butonuna bastığımızda gerçekleşmesini istediğimiz olaylar:
1- Arayüz üzerinde yazılmış ya da işaretlenmiş bilgileri input olarak alıyor.
2- Multiple_check ve valid_check methodlarını kullanrak kişinin oy vermeye uygun olup olmadığına bakıyor.
3- Eğer kişi uygunsa, bu bilgileri kullanarak bir Voter objesi yaratıyor(class konusu)
4- Oluşturulmuş olan objeyi(Oy veren kişinin bilgisi) voters listesine ekliyor. Böylece oy veren herkesin bilgileri bi listede toplanmış oluyor.
5- En sonda ise arayüzün fieldlarını temizleyerek bir sonraki kişi için hazır hale getiriyor.

"""
def oy_ver():
    voter_id = id_field.get()
    voter_isim = isim_field.get()
    voter_soyisim = soyisim_field.get()
    voter_lider = lider_isim_field.get()
    voter_lider = voter_lider.capitalize()

    if valid_check(voter_id):
        messagebox.showwarning("Error", "YetGen mensubu değilsiniz. Oyunuz geçerli değil.")
    elif multiple_check(voter_id):
        messagebox.showwarning("Error","Üzgünüz, sadece 1 kere oy kullanabilirsiniz.")
    else:
        voter_choice = seçim_var.get()
        voter = Voter(voter_id,voter_isim,voter_soyisim,voter_choice,voter_lider)
        voters.append(voter)
        messagebox.showinfo("Başarılı.","Oy verdiğiniz için teşekkür ederiz.")
    id_field.delete(0,tk.END)
    isim_field.delete(0,tk.END)
    soyisim_field.delete(0,tk.END)
    lider_isim_field.delete(0,tk.END)
    seçim_var.set(0)


"""
Arayüz oluşturma kısmı
"""
root = tk.Tk()
root.geometry("300x285")
root.title("13 Mayıs YetGen Seçimi")

id_label = tk.Label(root, text="YetGen ID:")
id_label.grid(row=0, column=0, padx=15,pady=5)

id_field = tk.Entry(root)
id_field.grid(row=0, column=1,padx=10,pady=5)

isim_label = tk.Label(root, text="İsim:")
isim_label.grid(row=1, column=0, padx=30, pady=5)
isim_field = tk.Entry(root)
isim_field.grid(row=1, column=1, padx=10, pady=5)

soyisim_label = tk.Label(root, text="Soyisim:")
soyisim_label.grid(row=2, column=0, padx=15, pady=5)
soyisim_field = tk.Entry(root)
soyisim_field.grid(row=2, column=1, padx=10, pady=5)

lider_isim_label = tk.Label(root, text="Lider adı:")
lider_isim_label.grid(row=3, column=0, padx=15, pady=5)
lider_isim_field = tk.Entry(root)
lider_isim_field.grid(row=3, column=1, padx=10, pady=5)

seçim_label = tk.Label(root, text="Seçiminizi yapınız:")
seçim_label.grid(row=4, column=0, padx=15, pady=5)
seçim_var = tk.StringVar(root, "a")
python_button = tk.Radiobutton(root, text="Python ittifakı", variable=seçim_var, value="a")
python_button.grid(row=4, column=1, padx=15, pady=5)
java_button = tk.Radiobutton(root, text="Java ittifakı", variable=seçim_var, value="b")
java_button.grid(row=5, column=1, padx=15, pady=5)

vote_button = tk.Button(root, text="Oy ver", command=oy_ver)
vote_button.grid(row=6, column=0, padx=5, pady=5)

end_button = tk.Button(root, text="Seçimi sonlandır", command=end_election)
end_button.grid(row=6, column=1, padx=5, pady=5)

root.mainloop()