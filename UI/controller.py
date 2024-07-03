import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        self._model.creaGrafo()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {self._model.numNodes()}, Numero archi: {self._model.numEdges()}"))
        self._view.txt_result.controls.append(ft.Text(f"Valore minimo: {self._model.minimo} Valore massimo: {self._model.massimo}"))
        self._view.update_page()

    def handle_countedges(self, e):
        self._view.txt_result2.controls.clear()
        try:
            soglia = float(self._view.txt_name.value)
        except:
            self._view.create_alert("Inserire un valore numerico")
            return
        if soglia > self._model.massimo or soglia < self._model.minimo:
            self._view.create_alert("Inserire valore compreso tra minimo e massimo")
        archiMinore, archiMaggiore = self._model.contaArchi(soglia)
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso maggiore: {len(archiMaggiore)}"))
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso minore: {len(archiMinore)}"))
        self._view.update_page()

    def handle_search(self, e):
        self._view.txt_result3.controls.clear()
        try:
            soglia = float(self._view.txt_name.value)
        except:
            self._view.create_alert("Inserire un valore numerico")
            return
        if soglia > self._model.massimo or soglia < self._model.minimo:
            self._view.create_alert("Inserire valore compreso tra minimo e massimo")
        self._model.cercaPercorso(soglia)
        self._view.txt_result3.controls.append(ft.Text(f"Peso cammino massimo: {self._model.bestPeso}"))
        for e in self._model.bestPath:
            self._view.txt_result3.controls.append(ft.Text(f"{e[0]} --> {e[1]}: {e[2]['weight']}"))
        self._view.update_page()