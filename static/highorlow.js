
        let users = [];
        let user = null;
        let deck = [];
        let currentCard = null;
    
        const suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'];
        const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
    
        async function fetchUsers() {
            try {
                const response = await fetch('/static/users.json');
                users = await response.json();
                console.log('Fetched Users:', users);
            } catch (error) {
                console.error('Failed to fetch user data:', error);
            }
        }

        async function saveUsers() {
            try {
                const response = await fetch('/api/save_users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(users)
                });
                const result = await response.json();
                console.log('Save Users Response:', result);
            } catch (error) {
                console.error('Failed to save user data:', error);
            }
        }

        function createDeck() {
            let deck = [];
            for (let suit of suits) {
                for (let value of values) {
                    deck.push({ suit, value });
                }
            }
            return deck;
        }

        function shuffleDeck(deck) {
            for (let i = deck.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [deck[i], deck[j]] = [deck[j], deck[i]];
            }
        }

        function drawCard() {
            return deck.pop();
        }

        function compareCards(oldCard, newCard, choice) {
            const oldValueIndex = values.indexOf(oldCard.value);
            const newValueIndex = values.indexOf(newCard.value);
            if (choice === 'higher') {
                return newValueIndex > oldValueIndex;
            } else {
                return newValueIndex < oldValueIndex;
            }
        }

        function guess(choice) {
            // Your existing guess logic
        }

        function login() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            user = users.find(u => u.username === username && u.password === password);
            if (user) {
                document.getElementById('login').style.display = 'none';
                document.getElementById('game').style.display = 'block';
                deck = createDeck();
                shuffleDeck(deck);
                currentCard = drawCard();
                updateUI();
            } else {
                alert('Invalid username or password');
            }
        }

        function updateUI() {
            document.getElementById('currentCard').innerText = `${currentCard.value} of ${currentCard.suit}`;
            document.getElementById('balance').innerText = `Balance: $${user.money}`;
        }

        fetchUsers();

        function guess(choice) {
            const newCard = drawCard();
            const result = compareCards(currentCard, newCard, choice);
            currentCard = newCard;
            updateUI();
            document.getElementById('result').innerText = result ? 'Correct!' : 'Wrong!';
            if (result) {
                user.money += 10;
            } else {
                user.money -= 10;
            }
            saveUsers();
        }

        fetchUsers();
