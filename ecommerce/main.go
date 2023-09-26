package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// Product struct represents a product with an ID and Detail.
type Product struct {
	Detail string `json:"detail"`
}

var products = map[string]Product{
	"f1d9fb02-a7da-44f6-8584-d9b00786bf38": {Detail: "Smart TV 65 4K LED LG 65UR8750PSA Para você que gosta de reunir a família e os amigos para assistir algum filme engraçado ou maratonar aquela série que prende a atenção de todos, precisa conhecer a Smart TV de 65 LG 65UR8750PSA. Ela possui resolução 4K Ultra HD com tecnologia LED onde você assiste os conteúdos favoritos em alta definição aprimorados com o AI 4K Upscaling, 60Hz de frequência, sistema operacional webOS 23 e processador α5 AI Processor 4K Gen6. Além disso, ainda oferece conectividade via Bluetooth e Wi-Fi que facilitam a conexão com outros dispositivos e periféricos, assistentes virtuais Alexa, Google e Apple, 3 entradas HDMI e 2 USB, ThinQ AI e HDR10. Essa é uma Smart TV completa para ser o centro das atenções da sua sala."},
	"5293b118-d8c2-4c63-b5bf-027eec118126": {Detail: "Notebook Vaio FE15 Intel Core i5 16GB 512GB SSD Nos dias de hoje, com o avanço constante da tecnologia, tudo o que for digital, nem sempre é resolvido somente com um smartphone e é necessário o uso de computadores ou notebooks. Muitos optam pelo notebook pela praticidade de poder trabalhar, navegar pela internet e estudar em qualquer lugar que estiver. Por isso, se você está a procura de um novo notebook, precisa conhecer o Vaio FE15 VJFE55F11X-B0611H. Ele tem processador Intel Core i5 de 11ª Geração, 16GB de memória RAM, 512GB de armazenamento SSD e armazenamento em nuvem com 1 ano de assinatura Dropbox com 100GB. A tela dele é em LED Widescreen de 15,6 com resolução Full HD (1920x1080). Conta com sistema operacional Linux Debian 10 e teclado com resistência a derramamento de água. E ainda, pesando 1,75kg, é leve pra levá-lo a qualquer lugar e cabe em uma bolsa ou mochila."},
}

func getProductDetail(w http.ResponseWriter, r *http.Request) {
	// Parse the product ID from the request URL
	id := strings.TrimPrefix(r.URL.Path, "/products/")

	// Lookup the product by ID
	product, found := products[id]
	if !found {
		http.NotFound(w, r)
		return
	}

	// Serialize the product as JSON and send it as the response
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(product)
}

func main() {
	http.HandleFunc("/products/", getProductDetail)

	fmt.Println("Server is running on :8080...")
	http.ListenAndServe(":8080", nil)
}
