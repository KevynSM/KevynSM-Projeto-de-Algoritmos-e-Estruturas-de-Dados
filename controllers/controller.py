from aed_ds.dictionaries.hash_table import HashTable
from aed_ds.lists.singly_linked_list import SinglyLinkedList
from models.profissional import Profissional
from models.utente import Utente
from models.family import Family
from models.servicos import Servico
import ctypes

class Controller:
    def __init__(self):
        # self.category_array = (3 * ctypes.py_object)() # Array of pointers        
        # for i in range(3):
        #     self.category_array[i] = HashTable()

        self.categories = HashTable()
        self.categories.insert("Medicina", HashTable())
        self.categories.insert("Enfermagem", HashTable())
        self.categories.insert("Auxiliar", HashTable())

        self.categories_list_ordered = SinglyLinkedList()
        self.categories_list_ordered.insert_last("Medicina")
        self.categories_list_ordered.insert_last("Enfermagem")
        self.categories_list_ordered.insert_last("Auxiliar")



        self.utente_universe = HashTable()
        
        self.family_universe = HashTable()

        self.servicos = HashTable()
        self.servicos.insert("Consulta",SinglyLinkedList())
        self.servicos.insert("PequenaCirurgia",SinglyLinkedList())
        self.servicos.insert("Enfermagem",SinglyLinkedList())

    
#-------------------------------- Booleans --------------------------------------------
    def has_utente(self, name):
        if self.utente_universe.has_key(name):
            return True
        return False

    def there_are_utentes(self):
        if self.utente_universe.size() > 0:
            return True
        return False

    def has_faixa_etaria(self, faixa_etaria):
        if faixa_etaria in ["Jovem", "Adulto", "Idoso"]:
            return True
        return False

    def has_that_family(self, family_name):        
        if self.family_universe.has_key(family_name):
            return True
        return False

    def has_family(self):
        if self.family_universe.size():
            return True
        return False
        
    def utente_has_family(self, name):
        if self.utente_universe.get(name).familia_associada != None:
            return True 
        return False

    def has_category(self, name):
        list_categories = self.categories.keys()
        it = list_categories.iterator()
        while it.has_next():
            current_item = it.next()
            if name == current_item:
                return True
        return False


    def has_profissional(self):
        list_keys = self.categories.keys()        
        it = list_keys.iterator()
        while it.has_next():
            current_item = it.next()
            if self.categories.get(current_item).size() > 0:
                return True
        return False

    def has_profissional_category(self, name, category):
        list_profissionais = self.categories.get(category).keys()
        it = list_profissionais.iterator()
        while it.has_next():
            current_item = it.next()
            if name == current_item:
                return True
        return False

    def has_service(self, name):
        list_servicos = self.servicos.keys()
        it = list_servicos.iterator()
        while it.has_next():
            current_item = it.next()
            if name == current_item:
                return True
        return False

    def service_has_category(self, service, category):
        if service == "Consulta":
            if category == "Medicina":
                return True
        elif service == "PequenaCirurgia":
            if category in ["Medicina", "Enfermagem", "Auxiliar"]:
                return True
        elif service == "Enfermagem":
            if category in ["Enfermagem", "Auxiliar"]:
                return True
        return False

    def has_valid_sequence(self, service_list):
        last_consulta = False
        last_pequena_cirurgia = False        
        it = service_list.iterator()
        while it.has_next():
            current_service = it.next()            
            if current_service.name == "Consulta":
                last_consulta = True
            if current_service.name == "PequenaCirurgia" and last_consulta == False:
                return False
            if current_service.name == "PequenaCirurgia":
                last_pequena_cirurgia = True
                last_consulta = False
            if last_pequena_cirurgia == True and current_service.name == "Consulta":
                last_pequena_cirurgia = False
        if last_pequena_cirurgia == True:
            return False
        return True

                
    def has_service_utente(self, utente):
        list_keys = self.utente_universe.get(utente).servicos.keys()
        it = list_keys.iterator()
        while it.has_next():
            current_key = it.next()
            if not(self.utente_universe.get(utente).servicos.get(current_key).is_empty()):
                return True
        return False
                





#------------------------------------ do something ----------------------------------
    def registrar_profissional(self, name, category):
        self.categories.get(category).insert(name,Profissional(name,category))

    def registrar_utente(self, name, faixa_etaria):
        self.utente_universe.insert(name,Utente(name,faixa_etaria))

    def registrar_familia(self, name):
        self.family_universe.insert(name,Family(name))

    def associar_utente_familia(self, name, family_name):
        # Associa o utente a familia
        self.family_universe.get(family_name).utentes_associados.insert_last(name)
        # Associa a familia ao utente
        self.utente_universe.get(name).familia_associada = family_name        

    def desassociar_utente_familia(self,name):
        # Desassocia o utente da familia
        family_name = self.utente_universe.get(name).familia_associada
        position = self.family_universe.get(family_name).utentes_associados.find(name)
        self.family_universe.get(family_name).utentes_associados.remove(position)
        # Desassocia a familia do utente
        self.utente_universe.get(name).familia_associada = None

    def listar_profissionais(self):
        #list that will be return
        list_profissionais = SinglyLinkedList()
        # list_categories = [Medicina, Enfermagem, Auxiliar]
        # list_categories = self.categories.keys()
        list_categories = self.categories_list_ordered
        # for each category
        it = list_categories.iterator()
        while it.has_next():
            #category name
            category = it.next()
            
            # list of names in the caregory
            list_names = self.categories.get(category).keys()
            list_names_size = list_names.size()
            
            if list_names_size > 0:
                # array_size = list_name_size
                profissionais_array = (list_names_size * ctypes.py_object)() # Array of pointers
                idx = -1
                # for each name in the category
                it_category = list_names.iterator()
                while it_category.has_next():
                    current_item = it_category.next()
                    
                    idx += 1 
                    
                    profissionais_array[idx] = current_item
                # order the array
                self.quicksort(profissionais_array, 0, idx, self.comp_strings)
                # pass the the names from the ordered array to the final list
                for i in range(idx+1):
                    list_profissionais.insert_last(f"{category} {profissionais_array[i]}")
        return list_profissionais

    def listar_utentes(self):
        # lsit that will be returned
        list_utentes = SinglyLinkedList()     
        list_itens = self.utente_universe.items()
        # 3 list to separate the "faixas etarias"
        list_jovens = SinglyLinkedList()
        list_adultos = SinglyLinkedList()
        list_idosos = SinglyLinkedList()
        # filing the lists
        it = list_itens.iterator()
        while it.has_next():
            current_item = it.next()
            if current_item.get_value().faixa_etaria == "Jovem":
                list_jovens.insert_last(current_item.get_value().name)
            elif current_item.get_value().faixa_etaria == "Adulto":
                list_adultos.insert_last(current_item.get_value().name)
            elif current_item.get_value().faixa_etaria == "Idoso":
                list_idosos.insert_last(current_item.get_value().name)
        # Create an array for each "faixa etaria" list
        list_jovens_size = list_jovens.size()
        jovens_array = (list_jovens_size * ctypes.py_object)() # Array of pointers
        list_adultos_size = list_adultos.size()
        adultos_array = (list_adultos_size * ctypes.py_object)() # Array of pointers
        list_idosos_size = list_idosos.size()
        idosos_array = (list_idosos_size * ctypes.py_object)() # Array of pointers
        # Passing the lists to an Array and ordering
        # jovens
        idx = -1
        it = list_jovens.iterator()
        while it.has_next():
            current_item = it.next()
            idx += 1
            jovens_array[idx] = current_item
        self.quicksort(jovens_array, 0, idx, self.comp_strings)
        # Adultos
        idx = -1
        it = list_adultos.iterator()
        while it.has_next():
            current_item = it.next()
            idx += 1
            adultos_array[idx] = current_item
        self.quicksort(adultos_array, 0, idx, self.comp_strings)
        # Idosos
        idx = -1
        it = list_idosos.iterator()
        while it.has_next():
            current_item = it.next()
            idx += 1
            idosos_array[idx] = current_item
        self.quicksort(idosos_array, 0, idx, self.comp_strings)
        # Create an ordered array of familis names
        # Exacly how it is in the function listar_familias()
        list_families = self.family_universe.keys()
        list_families_size = list_families.size()
        families_array = (list_families_size * ctypes.py_object)() # Array of pointers
        idx = -1
        # Passing the families from the linkedlist to an Array
        it = list_families.iterator()
        while it.has_next():
            current_item = it.next()
            idx += 1
            families_array[idx] = current_item
        # Ordering the array with families
        self.quicksort(families_array, 0, idx, self.comp_strings)

        # Print the Jovem-Adulto-Idoso order for each Family
        for i in range(list_families_size):
            for j in range(list_jovens_size):
                if families_array[i] == self.utente_universe.get(jovens_array[j]).familia_associada:
                    # print(f"{families_array[i]} Jovem {jovens_array[j]}")
                    list_utentes.insert_last(f"{families_array[i]} Jovem {jovens_array[j]}")
            
            for j in range(list_adultos_size):
                if families_array[i] == self.utente_universe.get(adultos_array[j]).familia_associada:
                    # print(f"{families_array[i]} Adulto {adultos_array[j]}")
                    list_utentes.insert_last(f"{families_array[i]} Adulto {adultos_array[j]}")

            for j in range(list_idosos_size):
                if families_array[i] == self.utente_universe.get(idosos_array[j]).familia_associada:
                    # print(f"{families_array[i]} Idoso {idosos_array[j]}")
                    list_utentes.insert_last(f"{families_array[i]} Idoso {idosos_array[j]}")

        # Print the utenes witchout families associated
        for i in range(list_jovens_size):
            if self.utente_universe.get(jovens_array[i]).familia_associada == None:
                # print(f"Jovem {jovens_array[i]}")
                list_utentes.insert_last(f"Jovem {jovens_array[i]}")
        
        for i in range(list_adultos_size):
            if self.utente_universe.get(adultos_array[i]).familia_associada == None:
                # print(f"Adulto {adultos_array[i]}")
                list_utentes.insert_last(f"Adulto {adultos_array[i]}")

        for i in range(list_idosos_size):
            if self.utente_universe.get(idosos_array[i]).familia_associada == None:
                # print(f"Idoso {idosos_array[i]}")
                list_utentes.insert_last(f"Idoso {idosos_array[i]}")
        return list_utentes

    
    def listar_familias(self):
        #list that will be returned
        list_families_final = SinglyLinkedList()
        list_families = self.family_universe.keys()
        list_families_size = list_families.size()
        
        families_array = (list_families_size * ctypes.py_object)() # Array of pointers
        idx = -1
        # Passing the families from the linkedlist to an Array
        it = list_families.iterator()
        while it.has_next():
            current_item = it.next()
            
            idx += 1
           
            families_array[idx] = current_item
        # Ordering the array with families        
        self.quicksort(families_array, 0, idx, self.comp_strings)
        # Print the families
        for i in range(list_families_size):
            list_families_final.insert_last(f"{families_array[i]}")
        return list_families_final



    def mostrar_familia(self, family_name):
        # lsit that will be returned
        list_family = SinglyLinkedList()
        list_itens = self.utente_universe.items()
        # 3 list to separate the "faixas etarias"
        list_jovens = SinglyLinkedList()
        list_adultos = SinglyLinkedList()
        list_idosos = SinglyLinkedList()
        # filing the lists
        it = list_itens.iterator()
        while it.has_next():
            current_item = it.next()
            if current_item.get_value().faixa_etaria == "Jovem":
                list_jovens.insert_last(current_item.get_value().name)
            elif current_item.get_value().faixa_etaria == "Adulto":
                list_adultos.insert_last(current_item.get_value().name)
            elif current_item.get_value().faixa_etaria == "Idoso":
                list_idosos.insert_last(current_item.get_value().name)
        # Create an array for each "faixa etaria" list
        list_jovens_size = list_jovens.size()
        jovens_array = (list_jovens_size * ctypes.py_object)() # Array of pointers
        list_adultos_size = list_adultos.size()
        adultos_array = (list_adultos_size * ctypes.py_object)() # Array of pointers
        list_idosos_size = list_idosos.size()
        idosos_array = (list_idosos_size * ctypes.py_object)() # Array of pointers
        # Passing the lists to an Array and ordering
        # jovens
        idx = -1
        it = list_jovens.iterator()
        while it.has_next():
            current_item = it.next()
            idx += 1
            jovens_array[idx] = current_item
        self.quicksort(jovens_array, 0, idx, self.comp_strings)
        # Adultos
        idx = -1
        it = list_adultos.iterator()
        while it.has_next():
            current_item = it.next()
            idx += 1
            adultos_array[idx] = current_item
        self.quicksort(adultos_array, 0, idx, self.comp_strings)
        # Idosos
        idx = -1
        it = list_idosos.iterator()
        while it.has_next():
            current_item = it.next()
            idx += 1
            idosos_array[idx] = current_item
        self.quicksort(idosos_array, 0, idx, self.comp_strings)
        # Print the Jovem-Adulto-Idoso order for the Family
        for j in range(list_jovens_size):
            if family_name == self.utente_universe.get(jovens_array[j]).familia_associada:
                # print(f"Jovem {jovens_array[j]}")
                list_family.insert_last(f"Jovem {jovens_array[j]}")
            
        for j in range(list_adultos_size):
            if family_name == self.utente_universe.get(adultos_array[j]).familia_associada:
                # print(f"Adulto {adultos_array[j]}")
                list_family.insert_last(f"Adulto {adultos_array[j]}")

        for j in range(list_idosos_size):
            if family_name == self.utente_universe.get(idosos_array[j]).familia_associada:
                #print(f"Idoso {idosos_array[j]}")
                list_family.insert_last(f"Idoso {idosos_array[j]}")

        return list_family




    def create_service(self, service, utente):
        return Servico(service, utente)

    def fill_service(self, service, profissional, category):
        service.profissionais.get(category).insert_last(profissional)


    # def marcar_cuidados_utente(self, service, new_service, utente, profissional, category):        
    #     # Marca service com o utente
    #     self.utente_universe.get(utente).servicos.get(service).insert_last(new_service)
    #     self.utente_universe.get(utente).last_service = service
    #     # Marca o service com o profissional
    #     self.categories.get(category).get(profissional).servicos.get(service).insert(utente, new_service)
    #     # Marcaro service na lista de services
    #     self.servicos.get(service).insert_last(new_service)

    def marcar_cuidados_utente(self, list_service, utente):            
        it = list_service.iterator()
        while it.has_next():            
            current_service = it.next()
            # variables needed = serviuce_name, service, utente, profissional, category
            # service = current_service
            # utente = OK
            # service_name:
            service_name = current_service.name
            # profissional e category
            list_profissionais_medicina = None
            list_profissionais_enfermagem = None
            list_profissionais_auxiliar = None
            if service_name == "Consulta":
                list_profissionais_medicina = current_service.profissionais.get("Medicina")
            elif service_name == "PequenaCirurgia":
                list_profissionais_medicina = current_service.profissionais.get("Medicina")
                list_profissionais_enfermagem = current_service.profissionais.get("Enfermagem")
                list_profissionais_auxiliar = current_service.profissionais.get("Auxiliar")
            elif service_name == "Enfermagem":
                list_profissionais_enfermagem = current_service.profissionais.get("Enfermagem")
                list_profissionais_auxiliar = current_service.profissionais.get("Auxiliar")

            # Marcar service com o utente
            self.utente_universe.get(utente).servicos.get(service_name).insert_last(current_service)
            # Marcar service na lista de servicos
            self.servicos.get(service_name).insert_last(current_service)
            # Marcar o service com os profissionais
            # Medicina
            if list_profissionais_medicina is not None:
                it_p = list_profissionais_medicina.iterator()
                while it_p.has_next():
                    current_profissional = it_p.next()
                    #existe key com nome do utente?
                    if not(self.categories.get("Medicina").get(current_profissional).servicos.get(service_name).has_key(utente)):
                        self.categories.get("Medicina").get(current_profissional).servicos.get(service_name).insert(utente, SinglyLinkedList())
                    # marca em cada profissional de medicina                                          
                    self.categories.get("Medicina").get(current_profissional).servicos.get(service_name).get(utente).insert_last(current_service)
                    # # marca em cada profissional de medicina
                    # self.categories.get("Medicina").get(current_profissional).servicos.get(service_name).insert(utente, current_service)
            # Enfermagem
            if list_profissionais_enfermagem is not None:
                it_p = list_profissionais_enfermagem.iterator()
                while it_p.has_next():
                    current_profissional = it_p.next()
                    #existe key com nome do utente?
                    if not(self.categories.get("Enfermagem").get(current_profissional).servicos.get(service_name).has_key(utente)):
                        self.categories.get("Enfermagem").get(current_profissional).servicos.get(service_name).insert(utente, SinglyLinkedList())
                    # marca em cada profissional de Enfermagem                                          
                    self.categories.get("Enfermagem").get(current_profissional).servicos.get(service_name).get(utente).insert_last(current_service)
                    # # marca em cada profissional de enfermagem
                    # self.categories.get("Enfermagem").get(current_profissional).servicos.get(service_name).insert(utente, current_service)
            # Auxiliar
            if list_profissionais_auxiliar is not None:
                it_p = list_profissionais_auxiliar.iterator()
                while it_p.has_next():
                    current_profissional = it_p.next()
                    #existe key com nome do utente?
                    if not(self.categories.get("Auxiliar").get(current_profissional).servicos.get(service_name).has_key(utente)):
                        self.categories.get("Auxiliar").get(current_profissional).servicos.get(service_name).insert(utente, SinglyLinkedList())
                    # marca em cada profissional de Auxiliar                                          
                    self.categories.get("Auxiliar").get(current_profissional).servicos.get(service_name).get(utente).insert_last(current_service)
                    # # marca em cada profissional de auxiliar
                    # self.categories.get("Auxiliar").get(current_profissional).servicos.get(service_name).insert(utente, current_service)


    def desmarcar_cuidado_utente(self, utente):
        # For each category service
        for service_category in ["Consulta", "PequenaCirurgia", "Enfermagem"]:
            # lista com os servicos de uma service_category
            list_service = self.utente_universe.get(utente).servicos.get(service_category)
            #Se essa lista nao estiver vazia
            if not(list_service.is_empty()):
                # for each servico de uma categoria de servico
                it = list_service.iterator()
                while it.has_next():
                    current_service = it.next()
                    # lista de profissionais de cada categoria por categoria de servico
                    if service_category == "Consulta":
                        list_profissionais_medicina = current_service.profissionais.get("Medicina")
                    elif service_category == "PequenaCirurgia":
                        list_profissionais_medicina = current_service.profissionais.get("Medicina")
                        list_profissionais_enfermagem = current_service.profissionais.get("Enfermagem")
                        list_profissionais_auxiliar = current_service.profissionais.get("Auxiliar")
                    elif service_category == "Enfermagem":
                        list_profissionais_enfermagem = current_service.profissionais.get("Enfermagem")
                        list_profissionais_auxiliar = current_service.profissionais.get("Auxiliar")

                if service_category in ["Consulta", "PequenaCirurgia"]:
                    # se a lista de profissinal nao estiver vazia
                    if not(list_profissionais_medicina.is_empty()):
                        # Para cara nome de profissional
                        it = list_profissionais_medicina.iterator()
                        while it.has_next():
                            current_profissional = it.next()
                            # remove o servico do profissional
                            self.categories.get("Medicina").get(current_profissional).servicos.get(service_category).remove(utente)

                if service_category in ["PequenaCirurgia", "Enfermagem"]:                    
                    # se a lista de profissinal nao estiver vazia
                    if not(list_profissionais_enfermagem.is_empty()):
                        # Para cara nome de profissional
                        it = list_profissionais_enfermagem.iterator()
                        while it.has_next():
                            current_profissional = it.next()
                            # remove o servico do profissional
                            self.categories.get("Enfermagem").get(current_profissional).servicos.get(service_category).remove(utente)

                    # se a lista de profissinal nao estiver vazia
                    if not(list_profissionais_auxiliar.is_empty()):
                        # Para cara nome de profissional
                        it = list_profissionais_auxiliar.iterator()
                        while it.has_next():
                            current_profissional = it.next()
                            # remove o servico do profissional
                            self.categories.get("Auxiliar").get(current_profissional).servicos.get(service_category).remove(utente)

               
            
            
            #deleto toda a lista de servicos de uma categoria de servico do utente 
            self.utente_universe.get(utente).servicos.get(service_category).make_empty()

            # lista para ter as posicoes contendo servicos com o utente
            list_positions = SinglyLinkedList()
            idx = -1
            # por cada servico
            it = self.servicos.get(service_category).iterator()
            while it.has_next():
                current_service = it.next()
                idx += 1
                # se o servico tiver o utente salva o idx do servico            
                if current_profissional.utente == utente:
                    list_positions.insert_last(idx)
            # para cada idx
            it = list_positions.iterator()
            while it.has_next():
                current_idx = it.next()
                # remove o servico do idx (idx dos servicos do utente)
                self.servicos.get(service_category).remove(current_idx)

# -----------------------------------quicksort ---------------------------    

    def comp_strings(self, a, b):
        for i in range(len(a)):
            if i >= (len(b)-1):
                return False
            elif a[i] < b[i]:
                return True
            elif a[i] > b[i]:
                return False
        return True

    def quicksort(self, l, left, right, comp):
        i = left
        j = right
        pivot = l[int((i+j)/2)]
        while i <= j:
            while comp(l[i], pivot) and i<len(l):
                i += 1
            while comp(pivot, l[j]) and j>-1:
                j -= 1
            if i <= j:
                tmp = l[j]
                l[j] = l[i]
                l[i] = tmp
                i += 1
                j -= 1
        if left < j:
            self.quicksort(l, left, j, comp)
        if i < right:
            self.quicksort(l, i, right, comp)