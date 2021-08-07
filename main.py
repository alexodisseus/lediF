import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

import operator
import os

ui = Gtk.Builder()
ui.add_from_file("principal.glade")

class ListaCategoriaRow(Gtk.ListBoxRow):

    def __init__(self,  page_name, icon_name):
        Gtk.ListBoxRow.__init__(self)
        self.categoria_add = page_name
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.set_border_width(6)
        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        box.pack_start(image, False, False, 0)
        label = Gtk.Label()
        label.set_text(page_name)
        box.pack_start(label, False, False, 0)
        self.add(box)

class ListaCategoriaAddRow(Gtk.ListBoxRow):

    def __init__(self,  page_name, icon_name):
        Gtk.ListBoxRow.__init__(self)
        self.categoria_add = page_name
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.set_border_width(6)
        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        box.pack_start(image, False, False, 0)
        label = Gtk.Label()
        label.set_text(page_name)
        box.pack_start(label, False, False, 0)
        self.add(box)


class ListaAppRow(Gtk.ListBoxRow):

    def __init__(self,  page_name, icon_name, doc_name):
        Gtk.ListBoxRow.__init__(self)
        self.page_widget = page_name
        self.page_widget2 = doc_name

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        box.set_border_width(6)
        image = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        box.pack_start(image, False, False, 0)
        label = Gtk.Label()
        label.set_text(page_name)
        box.pack_start(label, False, False, 0)
        self.add(box)

class Handler(object):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)
        self.categoria_remover = ''
        self.categoria_adicionar = ''
        self.categorias = []
        self.l = []
        self.lista_filtro = []
        self.carregar_apps()
        self.listar_apps()

        
    def listar_apps(self, *args):

        lista_box = ui.get_object("lista_aplicativos")
        list_box = ui.get_object("lista_categoria")
        todos_apps = lista_box.get_children()
        if self.categorias == []:
            print('ok')
            for x in self.l:
                self.categorias.append(x['Category'].rsplit(";"))
            lista = self.categorias
            newlist=[]
            for x in lista:
                for y in x:
                    
                    if y in newlist:
                        pass
                    else:
                        newlist.append(y)
            newlist.sort()
            self.categorias = newlist

        self.l.sort(key=operator.itemgetter('Name'))

        for x in self.l:
        
            if x['Name'] != None:
                nome = x['Name']
                
                if x['Icon']!=None and x['Icon']!=''  :
                    icon = x['Icon']
                else:
                    icon = " "
                lista_box.add(ListaAppRow((nome), icon, x['Doc'] ))
        lista_box.show_all()

   
    def carregar_apps(self,args=""):
        lista_box = ui.get_object("lista_aplicativos")
        print(args)    
        self.l = []
        if self.lista_filtro == []:
            cwd = "/usr/share/applications"
            dire = os.listdir(cwd)
            for y in dire:
                indice = {}
                if os.path.isdir('/usr/share/applications/'+y)==False:
                    nome = y.replace(".desktop","")
                    indice['Doc'] = nome
                    indice['Name'] = ""
                    indice['Icon'] = ""
                    indice['Category'] = ""
                    text = open('/usr/share/applications/'+y)
                    for x in text:
                        val = x.split()
                        if len(val)!=0:
                            if val[0][:5] == "Name=" and indice['Name'] == "":
                                indice['Name'] =  " ".join(val).replace("Name=","")
                            if val[0][:5] == "Icon=" and len(indice)!=0 and indice['Icon'] == "":
                                indice['Icon'] = val[0].replace("Icon=","")
                            if val[0][:5] == "Categ" and len(indice)!=0:
                                indice['Category'] = val[0].replace("Categories=","")
                    if indice['Name']!='':
                        self.lista_filtro.append(indice)
                    text.close()
            self.l=self.lista_filtro

        if args != '':    
            lista=[]        
            tam = len(args)
            for x in self.lista_filtro:
                cont = 0
                while cont < len(x['Name']):
                    if x['Name'][cont:tam+cont].lower() == args.lower():
                        lista.append(x)
                    cont = cont+1
            self.l = lista
        else:
            self.l=self.lista_filtro
            

    def app_selecionado(self,lista_box, row):

        menu_btn = ui.get_object("botaos")
        controle = ui.get_object("controle")
        remove = controle.get_children()
        self.app_selecionado = row.page_widget2
        texto_app = ui.get_object("texto_app")
        texto_app.set_text(row.page_widget)
        controle.remove(remove[0])
        controle.add(menu_btn)

    def editar_categoria_remove(self,lista,row):
        
        if row:
            self.categoria_remover = row.categoria_add
            

    def editar_app(self,*args):

        editar_nome = ui.get_object("editar_nome")
        editar_icone = ui.get_object("editar_icone")
        editar_categorias = ui.get_object("lista_categoria_add")
        
        lista_categoria = ui.get_object("lista_cateoria")
        if lista_categoria.get_children() ==[]:
            for x in self.categorias:
                if x == '':
                    pass
                else:
                    lista_categoria.add(ListaCategoriaRow((x), "list-add" ))
            
        text = open('/usr/share/applications/'+self.app_selecionado+".desktop")
        indice={}
        indice['Name']=''
        indice['Icone']=''
        indice['Categoria']=''
        for x in text:
            val = x.split()
            if len(val)!=0:
                if val[0][:5] == "Name=" and indice['Name'] == "":
                    indice['Name'] = " ".join(val).replace("Name=","")
                if val[0][:5] == "Icon=":
                    indice['Icone'] = val[0].replace("Icon=","")
                if val[0][:5] == "Categ":
                    indice['Categoria'] = val[0].replace("Categories=","").rsplit(";")               
            
        text.close()
        

        if indice['Icone']=='':
            editar_icone.set_from_icon_name("xviewer",2)
        else:
            editar_icone.set_from_icon_name(indice['Icone'],2)
        
        editar_nome.set_text("Nome: "+indice['Name'])
        
        for x in indice['Categoria']:
            if x == '':
                pass
            else:
                editar_categorias.add(ListaCategoriaAddRow((x), "dialog-close" ))
        

        win = ui.get_object("editar_app")
        win.show_all()

    def on_destroy_editar(self, *args):

        editar_categorias = ui.get_object("lista_categoria_add")
        remove = editar_categorias.get_children()
        
        for x in remove:
            editar_categorias.remove(x)
        
        win = ui.get_object("editar_app")
        win.hide()
        return True

    def buscar_app_filtro(self,*args):
        lista_box = ui.get_object("lista_aplicativos")
        todos_apps = lista_box.get_children()
        for x in todos_apps:
            lista_box.remove(x)
        busca = ui.get_object("buscar_app")
        busca = busca.get_text()
        self.carregar_apps(busca)
        self.listar_apps()

    def editar_gravar(self, *args):
        editar_categorias = ui.get_object("lista_categoria_add")
        editar_categorias = editar_categorias.get_children()
        check_categoria = False
        gravar=[]
        categorias=[]
        text = open('/usr/share/applications/'+self.app_selecionado+".desktop")
        for x in text:
            val = x.split()
            if len(val)!=0:
                if val[0][:5] == "Categ":
                    check_categoria = True
                    categorias = ['Categories=']
                    for x in editar_categorias:
                        categorias.append(x.categoria_add+';')
                    categorias = "".join(categorias)
                    gravar.append([categorias])
                else:                   
                    gravar.append(val)
        if check_categoria == False and len(editar_categorias)>0:
            categorias = ['Categories=']
            for x in editar_categorias:
                categorias.append(x.categoria_add+';')
            categorias = "".join(categorias)
            gravar.append([categorias])
        text.close()
        text = open('/usr/share/applications/'+self.app_selecionado+".desktop" ,"w")
        for x in gravar:
            a=0
            for y in x:
                if a ==0:
                    a=1
                    text.write(str(y))
                else:
                    text.write(str(" "))
                    text.write(str(y))
            text.write('\n')   
        text.close()
        self.retorno_ok()
        
    def adicionar_categoria(self,*args):

        editar_categorias = ui.get_object("lista_categoria_add")
        if self.categoria_adicionar != '':
            editar_categorias.add(ListaCategoriaAddRow((self.categoria_adicionar), "dialog-close" ))
            editar_categorias.show_all()
        self.categoria_adicionar = ''

    def remover_categoria(self,*args):
        editar_categorias = ui.get_object("lista_categoria_add")
        remove = editar_categorias.get_children()
        for x in remove:
            if self.categoria_remover ==x.categoria_add:
                editar_categorias.remove(x)    
                print('REMOVE '+x.categoria_add)
        self.categoria_remover = ''

    def editar_categoria_add(self,lista,row):
        if row:
            self.categoria_adicionar = row.categoria_add
            print(self.categoria_adicionar)

    def onDestroy(self, *args):
        Gtk.main_quit()        
    def sobre(self, *args):
        win = ui.get_object("janela_sobre")
        win.show_all()
    
    def sobreDestroy(self, *args):

        win = ui.get_object("janela_sobre")
        win.hide()
        return True
    def retornoDestroy(self, *args):
        
        win = ui.get_object("retorno_ok")
        win.hide()
        return True
        
    def retorno_ok(self, *args):
        win = ui.get_object("retorno_ok")
        win.show_all()


ui.connect_signals(Handler())
window = ui.get_object("principal")
window.show_all()

Gtk.main()

