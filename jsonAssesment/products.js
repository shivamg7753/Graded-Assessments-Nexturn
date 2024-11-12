const jsonData = `[
  {"id": 1, "name": "Laptop", "category": "Electronics", "price": 1500, "available": true},
  {"id": 2, "name": "Phone", "category": "Electronics", "price": 700, "available": false},
  {"id": 3, "name": "Table", "category": "Furniture", "price": 300, "available": true}
]`;


function parseData(json) {
  try {
    return JSON.parse(json);
  } catch (error) {
    console.error("Error parsing JSON data:", error);
    return [];
  }
}

let products = parseData(jsonData);


function addProduct(newProduct) {
  products.push(newProduct);
  console.log("Product added successfully.");
}


function updatePrice(productId, newPrice) {
  const product = products.find(p => p.id === productId);
  if (product) {
    product.price = newPrice;
    console.log("Product price updated successfully.");
  } else {
    console.error("Product not found.");
  }
}

function filterAvailableProducts() {
  return products.filter(p => p.available);
}

function filterProductsByCategory(category) {
  return products.filter(p => p.category === category);
}

addProduct({ id: 4, name: "Chair", category: "Furniture", price: 120, available: true });

updatePrice(1, 1400);

console.log("Available Products:", filterAvailableProducts());

console.log("Electronics:", filterProductsByCategory("Electronics"));