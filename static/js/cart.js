function updateQuantity(itemId, newQuantity) {
  if (newQuantity < 1) return;

  fetch(`/api/cart/update/${itemId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ quantity: newQuantity }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        if (data.cart_count !== undefined) {
          updateCartBadge(data.cart_count);
        }
        location.reload();
      } else {
        alert(data.message || "Gagal mengupdate quantity");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Terjadi kesalahan saat mengupdate quantity");
    });
}

function removeFromCart(itemId) {
  if (confirm("Hapus item ini dari keranjang?")) {
    fetch(`/api/cart/remove/${itemId}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          if (data.cart_count !== undefined) {
            updateCartBadge(data.cart_count);
          }
          location.reload();
        } else {
          alert(data.message || "Gagal menghapus item");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Terjadi kesalahan saat menghapus item");
      });
  }
}

function toggleSelectAll() {
  const selectAllCheckbox = document.getElementById("selectAll");
  const itemCheckboxes = document.querySelectorAll(".item-checkbox");

  itemCheckboxes.forEach((checkbox) => {
    checkbox.checked = selectAllCheckbox.checked;
  });

  updateOrderSummary();
}

function updateOrderSummary() {
  const itemCheckboxes = document.querySelectorAll(".item-checkbox:checked");
  let subtotal = 0;
  let selectedCount = 0;

  itemCheckboxes.forEach((checkbox) => {
    const price = Number.parseFloat(checkbox.dataset.price);
    const quantity = Number.parseInt(checkbox.dataset.quantity);
    subtotal += price * quantity;
    selectedCount++;
  });

  const tax = subtotal * 0.1;
  const total = subtotal + tax;

  // Update display
  document.getElementById("selectedCount").textContent = selectedCount;
  document.getElementById("displaySubtotal").textContent =
    "Rp " + subtotal.toLocaleString("id-ID", { maximumFractionDigits: 0 });
  document.getElementById("displayTax").textContent =
    "Rp " + tax.toLocaleString("id-ID", { maximumFractionDigits: 0 });
  document.getElementById("displayTotal").textContent =
    "Rp " + total.toLocaleString("id-ID", { maximumFractionDigits: 0 });

  // Update select all checkbox state
  const allCheckboxes = document.querySelectorAll(".item-checkbox");
  const selectAllCheckbox = document.getElementById("selectAll");
  if (selectAllCheckbox && allCheckboxes.length > 0) {
    selectAllCheckbox.checked = allCheckboxes.length === itemCheckboxes.length;
  }
}

function proceedToCheckout() {
  const itemCheckboxes = document.querySelectorAll(".item-checkbox:checked");

  if (itemCheckboxes.length === 0) {
    // Show error message at the top of the page
    const existingError = document.querySelector(".checkout-error");
    if (existingError) {
      existingError.remove();
    }

    const errorDiv = document.createElement("div");
    errorDiv.className =
      "checkout-error bg-red-100 border border-red-400 text-red-700 px-6 py-4 rounded-lg mb-4";
    errorDiv.textContent = "Silakan pilih item untuk checkout";

    const mainContent = document.querySelector(".max-w-7xl");
    if (mainContent) {
      mainContent.insertBefore(errorDiv, mainContent.firstChild);
    }

    setTimeout(() => {
      errorDiv.remove();
    }, 3000);
    return;
  }

  const selectedItems = [];
  itemCheckboxes.forEach((checkbox) => {
    const itemId = checkbox.getAttribute("data-item-id");
    if (itemId) {
      selectedItems.push(itemId);
    }
  });

  // Navigate to checkout with selected items
  window.location.href = `/checkout?items=${selectedItems.join(",")}`;
}

function updateCartBadge(count) {
  const badge = document.querySelector(".cart-count");
  if (badge) {
    badge.textContent = count;
  }
}
