async function donate(charityId) {
    if (typeof window.ethereum !== "undefined") {
        const web3 = new Web3(window.ethereum);
        await window.ethereum.enable();

        const accounts = await web3.eth.getAccounts();
        const amount = document.getElementById("amount").value;
        const charityAddress = "0xYourCharityWalletAddress"; // Replace with actual charity Ethereum address

        web3.eth.sendTransaction({
            from: accounts[0],
            to: charityAddress,
            value: web3.utils.toWei(amount, "ether")
        })
        .on("transactionHash", function(hash) {
            document.getElementById("status").innerText = "Transaction Sent! Hash: " + hash;

            // Save transaction in Django database
            fetch('/save-donation/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    charity_id: charityId,
                    donor_address: accounts[0],
                    amount: amount,
                    transaction_hash: hash
                })
            });
        })
        .on("error", function(error) {
            document.getElementById("status").innerText = "Transaction Failed!";
        });
    } else {
        alert("MetaMask is not installed!");
    }
}

// Get CSRF token for Django AJAX
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
