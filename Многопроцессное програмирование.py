from multiprocessing import Manager, Process

class WarehouseManager:
    def __init__(self):
        self.data = Manager().dict()

    def process_request(self, request):
        product, action, quantity = request

        if action == 'receipt':
            if product not in self.data:
                self.data[product] = 0
            self.data[product] += quantity
        elif action == 'shipment':
            if product in self.data and self.data[product] >= quantity:
                self.data[product] -= quantity

    def run(self, requests):
        processes = []
        for request in requests:
            process = Process(target=self.process_request, args=(request,))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()


if __name__ == '__main__':
    manager = WarehouseManager()


    requests = [
    ("product1", "receipt", 100),
    ("product2", "receipt", 150),
    ("product1", "shipment", 30),
    ("product3", "receipt", 200),
    ("product2", "shipment", 50)
    ]

    manager.run(requests)

    print(manager.data)