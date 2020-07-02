from controllers.controller import Controller
from aed_ds.lists.singly_linked_list import SinglyLinkedList
# Comand Line Interface 
class CLI:
    def __init__(self):
        controller = Controller()

        while True:
            line = input()

            if line == "":
                exit()

            commands = line.split(" ") 

            # Registrar Profissional
            if commands[0] == "RP":
                category = commands[1]
                name = commands[2]
                if controller.has_category(category):
                    if not(controller.has_profissional_category(name, category)):
                        controller.registrar_profissional(name, category)
                        print("Profissional registrado com sucesso")
                    else:
                        print("Profissinal existente.")
                else:
                    print("Categoria Inexistente.")
                

            # Registrar Utente
            elif commands[0] == "RU":
                name = commands[1]
                faixa_etaria = commands[2]
                if not(controller.has_utente(name)):
                    if controller.has_faixa_etaria(faixa_etaria):
                        controller.registrar_utente(name, faixa_etaria)
                        print("Utente registrado com sucesso.")
                    else:
                        print("Faixa etaria inexistente.")
                else:
                    print("Utente existente.")
                

            # Registrar Familia
            elif commands[0] == "RF":
                family_name = commands[1]
                if not(controller.has_that_family(family_name)):
                    controller.registrar_familia(family_name)
                    print("Familia registrada com sucesso.")
                else:
                    print("Familia existente.")
                

            # Associar Utente de Familia
            elif commands[0] == "AF":
                name = commands[1]
                family_name = commands[2]
                if controller.has_utente(name):
                    if controller.has_that_family(family_name):
                        if not(controller.utente_has_family(name)):
                            controller.associar_utente_familia(name, family_name)                            
                            print("Utente associado a familia.")
                        else:
                            print("Utente percente a familia.")
                    else:
                        print("Familia inexistente.")
                else:
                    print("Utente inexistente.")
                 

            # Disassoiar Utente a Familia
            elif commands[0] == "DF":
                name = commands[1]
                if controller.has_utente(name):
                    if controller.utente_has_family(name):
                        controller.desassociar_utente_familia(name)
                        print("Utente desassociado da familia.")
                    else:
                        print("Utente nao pertence a familia.")
                else:
                    print("Utente inexistente.")
                

            # Listar Profissionais
            elif commands[0] == "LP":
                if controller.has_profissional():
                    list_profissionais = controller.listar_profissionais()
                    it = list_profissionais.iterator()
                    while it.has_next():
                        current_item =  it.next()
                        print(current_item)                    
                else:
                    print("Sem profissional registrado.")
                

            # Listar Utentes
            elif commands[0] == "LU":
                controller.listar_utentes()

            # Listar Familias
            elif commands[0] == "LF":
                if controller.has_family():
                    list_families = controller.listar_familias()
                    it = list_families.iterator()
                    while it.has_next():
                        current_item = it.next()
                        print(f"{current_item}.")
                else:
                    print("Sem famílias registradas.")

            # Mostrar Familia
            elif commands[0] == "MF":
                family_name = commands[1]
                controller.mostrar_familia(family_name)


            # Marcar Cuidados a Utente
            elif commands[0] == "MC":
                name = commands[1]
                if controller.has_utente(name):
                    list_services = SinglyLinkedList()
                    while True:
                        service = input()
                        if service == "":
                            break
                        if controller.has_service(service):
                            # Cria o servico
                            new_service = controller.create_service(service, name)
                            all_good = False
                            #Preenche o servico
                            while True:
                                new_line = input()
                                if new_line == "":
                                    break
                                categoria_profissinal = new_line.split(" ")
                                categoria = categoria_profissinal[0]
                                profissional = categoria_profissinal[1]
                                if controller.has_category(categoria):
                                    if controller.has_profissional_category(profissional, categoria):
                                        if controller.service_has_category(service, categoria):
                                            controller.fill_service(new_service, profissional, categoria)
                                            all_good = True
                                        else:
                                            print("Categoria inválida.")                                            
                                    else:
                                        print("Profissinal de saude inexistente.")                                        
                                else:
                                    print("Categoria inexistente.")                                    
                            # Se tudo der certo
                            # Marca o servico ao utente e ao profissional
                            if all_good:
                                list_services.insert_last(new_service)
                                # controller.marcar_cuidados_utente(service, new_service, name, profissional, categoria)
                                # print("Cuidados marcados com sucesso.")
                        else:
                            print("Serviço Inexistente.")
                            break
                else:
                    print("Utente Inexistente.")

            # # Marcar Cuidados a Utente
            # elif commands[0] == "MC":
            #     name = commands[1]
            #     if controller.has_utente(name):
            #         while True:
            #             service = input()
            #             if service == "":
            #                 break
            #             if controller.has_service(service):
            #                 # Cria o servico
            #                 new_service = controller.create_service(service, name)
            #                 all_good = False
            #                 #Preenche o servico
            #                 while True:
            #                     new_line = input()
            #                     if new_line == "":
            #                         break
            #                     categoria_profissinal = new_line.split(" ")
            #                     categoria = categoria_profissinal[0]
            #                     profissional = categoria_profissinal[1]
            #                     if controller.has_category(categoria):
            #                         if controller.has_profissional_category(profissional, categoria):
            #                             if controller.service_has_category(service, categoria):
            #                                 if controller.has_valid_sequence(name, service):
            #                                     controller.fill_service(new_service, profissional, categoria)
            #                                     all_good = True
            #                                 else:
            #                                     print("Sequencia inválida.")                                                
            #                             else:
            #                                 print("Categoria inválida.")                                            
            #                         else:
            #                             print("Profissinal de saude inexistente.")                                        
            #                     else:
            #                         print("Categoria inexistente.")                                    
            #                 # Se tudo der certo
            #                 # Marca o servico ao utente e ao profissional
            #                 if all_good:
            #                     controller.marcar_cuidados_utente(service, new_service, name, profissional, categoria)
            #                     print("Cuidados marcados com sucesso.")
            #             else:
            #                 print("Serviço Inexistente.")
            #                 break
            #     else:
            #         print("Utente Inexistente.")

            # Cancelar Cuidados Marcados a Utente
            elif commands[0] == "CC":
                name = commands[1]
                if controller.has_utente(name):
                    if controller.has_service_utente(name):
                       controller.desmarcar_cuidado_utente(name)
                       print("Cuidados de saúde desmacados com sucesso.")
                    else:
                        print("Utente sem cuidados de saúde marcados.")
                else:
                    print("Utente inexistente.")

            # Listar Cuidados Marcados a Utente
            elif commands[0] == "LCU":
                name = commands[1]
                pass

            # Listar Cuidados Marcados a Familia
            elif commands[0] == "LCF":
                family_name = commands[1]
                pass

            # Listar Servicos Marcados a Profissionais
            elif commands[0] == "LSP":
                category = commands[1]
                name = commands[2]
                pass

            # Listar Marcacoes por tipo de Servico
            elif commands[0] == "LMS":
                service = commands[1]
                pass

            # Gravar
            elif commands[0] == "G":
                file = commands[1]
                pass

            # Ler
            elif commands[0] == "L":
                file = commands[1]
                pass
            
            else:
                print("Instrução invalida.")