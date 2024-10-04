import re

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, node, key):
        if not node:
            return AVLNode(key)
        elif key < node.key:
            node.left = self.insert(node.left, key)
        else:
            node.right = self.insert(node.right, key)

        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        balance = self.get_balance(node)

        # Balanceamento
        if balance > 1:
            if key < node.left.key:
                return self.right_rotate(node)
            else:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)

        if balance < -1:
            if key > node.right.key:
                return self.left_rotate(node)
            else:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)

        return node

    def search(self, node, key):
        if not node or node.key == key:
            return node
        elif key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def in_order_traversal(self, node):
        res = []
        if node:
            res = self.in_order_traversal(node.left)
            res.append(node.key)
            res = res + self.in_order_traversal(node.right)
        return res


class Browser:
    def __init__(self):
        self.sitemap = AVLTree()
        self.visit_history = []
        self.current_page = None

    def load_urls(self, filename):
        try:
            with open(filename, 'r') as file:
                for url in map(str.strip, file):
                    if self.is_valid_url(url):
                        self.add_url(url)
            print("URLs carregadas.")
        except FileNotFoundError:
            print(f"Erro: {filename} não encontrado.")

    def is_valid_url(self, url):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  
            r'|(?:'  
            r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  
            r'localhost|'  
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  
            r'(?::\d+)?'  
            r'(?:/?|[/?]\S+)?$', re.IGNORECASE)
        return re.match(regex, url) is not None

    def add_url(self, url):
        if self.is_valid_url(url):
            if not self.sitemap.search(self.sitemap.root, url):
                self.sitemap.root = self.sitemap.insert(self.sitemap.root, url)
                print(f"URL {url} adicionada.")
            else:
                print("URL já existente.")
        else:
            print("Formato de URL inválido.")

    def show_history(self):
        print(f"Histórico de Visitas: {' -> '.join(self.visit_history) if self.visit_history else '[ ]'}")

    def navigate(self, url):
        if url.startswith("/") and self.current_page:
            full_url = self.current_page + url
        else:
            full_url = url

        if self.sitemap.search(self.sitemap.root, full_url):
            if self.current_page:
                self.visit_history.append(self.current_page)
            self.current_page = full_url
            print(f"Página encontrada! Home: [{self.current_page}]")
        else:
            print("Página não encontrada.")

    def back(self):
        if self.visit_history:
            self.current_page = self.visit_history.pop()
            print(f"Retornando à página: {self.current_page}")
        else:
            self.current_page = None
            print("Não há páginas anteriores.")

    def show_sitemap(self):
        urls = self.sitemap.in_order_traversal(self.sitemap.root)
        print("Sitemap: ", " -> ".join(urls) if urls else "[Vazio]")

    def help_command(self):
        print("""\
        Comandos disponíveis:
        #add <url>  : Adiciona uma nova URL ao sitemap
        #back       : Retorna à última página visitada
        #showhist   : Mostra o histórico de navegação
        #showsitemap: Mostra o sitemap
        #sair       : Encerra o navegador
        #help       : Exibe esta ajuda
        """)

    def run(self):
        # Carregar URLs do arquivo 'urls.txt' ao iniciar
        self.load_urls('urls.txt')
        while True:
            print(f"\nHome: [{self.current_page if self.current_page else ' '}]")
            user_input = input("Digite a url ou #back, #showhist, #showsitemap, #add <url>, #help, #sair: ").strip()

            if user_input.startswith("#add "):
                self.add_url(user_input[5:].strip())
            elif user_input == "#back":
                self.back()
            elif user_input == "#showhist":
                self.show_history()
            elif user_input == "#showsitemap":
                self.show_sitemap()
            elif user_input == "#help":
                self.help_command()
            elif user_input == "#sair":
                break
            else:
                self.navigate(user_input)


# Inicia o navegador
if __name__ == "__main__":
    browser = Browser()
    browser.run()
