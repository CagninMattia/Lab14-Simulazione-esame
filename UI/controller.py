import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._view.update_page()
        self._model.crea_grafo()
        num_nodi = self._model.num_nodi()
        num_archi = self._model.num_archi()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {num_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {num_archi}"))
        min, max = self._model.min_max_archi()
        self._view.txt_result.controls.append(ft.Text(f"Informazioni su pesi archi. Valore minimo: {min} Valore massimo: {max}"))
        self._view.btn_search.disabled = False
        self._view.txt_name.disabled = False
        self._view.btn_countedges.disabled = False
        self._view.update_page()


    def handle_countedges(self, e):
        soglia = self._view.txt_name.value
        if soglia is not None:
            try:
                soglia.replace(",", ".")
                soglia = float(soglia)
            except ValueError:
                self._view.txt_result2.controls.clear()
                self._view.create_alert("Inserisci un numero. ")
                self._view.update_page()
                return
            self._view.txt_result2.controls.clear()
            self._view.update_page()
            inf, sup = self._model.soglia(soglia)
            self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso maggiore della soglia: {sup}"))
            self._view.txt_result2.controls.append(ft.Text(f"Numero archi con peso minore della soglia: {inf}"))
            self._view.update_page()
        else:
            self._view.txt_result2.controls.clear()
            self._view.create_alert("Campo nullo. ")
            self._view.update_page()

    def handle_search(self, e):
        soglia = self._view.txt_name.value
        if soglia is not None:
            try:
                soglia.replace(",", ".")
                soglia = float(soglia)
            except ValueError:
                self._view.txt_result3.controls.clear()
                self._view.create_alert("Inserisci un numero. ")
                self._view.update_page()
                return
            self._view.txt_result3.controls.clear()
            self._view.update_page()
            peso_cammino, lista_archi_cammino= self._model.ricerca_cammino(soglia)
            self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: {peso_cammino}"))
            for arco in lista_archi_cammino:
                self._view.txt_result3.controls.append(ft.Text(f"{arco[0]} --> {arco[1]}: {arco[2]}"))
            self._view.update_page()
        else:
            self._view.txt_result3.controls.clear()
            self._view.create_alert("Campo nullo. ")
            self._view.update_page()