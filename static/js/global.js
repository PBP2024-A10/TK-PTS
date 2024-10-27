// var addFoodItemUrl = "/editors-choice/add/";

/**
 * Document-ready functions go here
 */
$(document).ready(function() {    
    /**
     * navbar Module / Page JS methods
     */
    // Update navbar links based on the current page
    function updateNavbarLinks() {
        const currentPath = window.location.pathname;
        const homepageUrl = "/"; // Change this to your homepage URL

        // List of pages where the href should be "#"
        const specialPages = ["/"];

        // Update the href attributes
        $('nav a#web-logo-anchor').each(function() {
            if (specialPages.includes(currentPath)) {
                $(this).attr('href', '#');
            } else {
                $(this).attr('href', homepageUrl);
            }
        });
    }
    updateNavbarLinks();

    async function updateUserMenu() {
        const userMenu = $('#user-menu');
        const logoutUrl = userMenu.data('logout-url');
        const loginUrl = userMenu.data('login-url');
        const registerUrl = userMenu.data('register-url');
        const username = userMenu.data('username');
        const usernameUrl = userMenu.data('username-url');

        try {
            const response = await fetch("/editors-choice/check-loggedin/");
            const data = await response.json();
            const isLoggedIn = data.is_logged_in;


            if (isLoggedIn) {
                userMenu.html(`
                    <a href="${usernameUrl}" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1" id="user-menu-item-0">Your Profile, ${username}</a>
                    <a href="${logoutUrl}" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1" id="user-menu-item-2">Sign out</a>
                `);
            } else {
                userMenu.html(`
                    <a href="${loginUrl}" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1" id="user-menu-item-0">Sign in</a>
                    <a href="${registerUrl}" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1" id="user-menu-item-1">Create account</a>
                `);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }
    updateUserMenu();

    // Track the state of the profile dropdown
    let isUserMenuVisible = false;

    // Toggle the profile dropdown
    $('#user-menu-button').on('click', function(event) {
        event.stopPropagation();
        if (isUserMenuVisible) {
            $('#user-menu').addClass('hidden opacity-0 scale-95').removeClass('opacity-100 scale-100');
        } else {
            $('#user-menu').removeClass('hidden opacity-0 scale-95').addClass('opacity-100 scale-100');
        }
        isUserMenuVisible = !isUserMenuVisible;
    });

    // Hide the profile dropdown when clicking outside
    $(document).on('click', function(event) {
        if (!$(event.target).closest('#user-menu-button').length && !$(event.target).closest('#user-menu').length) {
            $('#user-menu').addClass('hidden opacity-0 scale-95').removeClass('opacity-100 scale-100');
            isUserMenuVisible = false;
        }
    });
    
    /**
     * editors_choice Module / Page JS methods
     */
    // Update the add-food button when the user is a superuser (index page)
    async function superuserFeaturesIndex() {
        document.getElementById("addEditorChoice").innerHTML = "";
        document.getElementById("addEditorChoice").className = "";

        const response = await fetch("/editors-choice/check-superuser/");

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        } else if (response.ok) {
            const data = await response.json();
            if (data.is_superuser) {
                let buttonClass = "mb-4";
                let buttonhtml = `
                <a href="${addFoodItemUrl}">
                    <button class="bg-brown-darker hover:bg-brown-mild text-white px-4 py-2 rounded-lg transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105">Add Editor's Choice</button>
                </a>`;
                document.getElementById("addEditorChoice").className = buttonClass;
                document.getElementById("addEditorChoice").innerHTML = buttonhtml;
            }
        }
    }

    // Update the delete-food button and edit-rating button when the user is a superuser (food item page)
    async function superuserFeaturesFoodItem() {
        const template = document.getElementById("optionDiv");
        const response = await fetch("/editors-choice/check-superuser/");

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        } else {
            const data = await response.json();
            if (data.is_superuser) {
                // Extract food_id from URL
                const urlParams = new URLSearchParams(window.location.search);
                const foodItemId = urlParams.get('food_id');

                // Fetch from the full FoodRecommendation json database
                const responseFR = await fetch(`/editors-choice/json/food-rec/`);
                const dataFR = await responseFR.json();

                // Find the food item in the FoodRecommendation database
                const foodItem = dataFR.find(item => item.fields.food_item === foodItemId);
                const urlDeleteFoodRec = `/editors-choice/delete-food/?food_recommendation_id=${foodItem.pk}`;
            
                // If the food item is found, display the delete and edit buttons
                template.innerHTML += `
                <button data-modal-target="crudModal" data-modal-toggle="crudModal" class="mt-5 flex w-full items-center justify-center rounded-md border border-transparent bg-brown-darkest px-8 py-3 text-base font-medium text-white hover:bg-brown-darker focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105 cursor-pointer" onclick="showModal();">
                    Edit food-rating
                </button>
                <a href=${urlDeleteFoodRec} id="deleteFoodRec class="mt-5 flex w-full items-center justify-center rounded-md border border-transparent bg-red-700 px-8 py-3 text-base font-medium text-white hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105 cursor-pointer">
                    <button class="mt-5 flex w-full items-center justify-center rounded-md border border-transparent bg-red-700 px-8 py-3 text-base font-medium text-white hover:bg-red-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition duration-300 ease-in-out transform hover:-translate-y-1 hover:scale-105 cursor-pointer">Delete food-recommendation</button>
                </a>
                `;
            }
        }
    }

    // Superfunction to superuser features functions
    async function superuserFeatures() {
        superuserFeaturesIndex();
        superuserFeaturesFoodItem();
    }
    superuserFeatures();

    // Fetch the food types and display the editor's choice foods per given document url
    async function fetchFoodTypes(url) {
        try {
            let response;
            if (! url.includes('editors-choice/show/breakfast') && ! url.includes('editors-choice/show/lunch') && ! url.includes('editors-choice/show/dinner') && ! url.includes('editors-choice/show/souvenir')) {
                response = await fetch('/editors-choice/json/editor-choice/');
                foodType = 'all';
            } else {
                response = await fetch(`/editors-choice/json/editor-choice/${foodType}`);
            }
            const data = await response.json();
            fetchFoodFinisher(data, foodType);
        } catch (error) {
            console.error('Error fetching data:', error);
            document.getElementById('editorChoiceList').innerHTML = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <img src="/static/images/cross-mark-no-data.png" alt="No data" class="w-32 h-32 mb-4"/>
                <p class="text-center text-gray-600 mt-4">Data are not inputted yet or failed to connect.</p>
            </div>
            `;
            editorChoiceDesc.innerHTML = "Bali offers a wide range of food types, from traditional Balinese cuisine to international dishes. Here are some of the halal editor's choice foods in Bali.";
        }
    }
    fetchFoodTypes(document.URL);
});

/** 
 * Support methods go here
 */
// Fetch the food items based on the food item IDs
async function fetchFoodFinisher(data, foodType) {
    const editorChoiceList = document.getElementById('editorChoiceList');
    const editorChoiceDesc = document.getElementById('editorChoiceDesc');
    editorChoiceList.innerHTML = ''; // Clear the existing content

    if (data.length === 0) {
        editorChoiceList.innerHTML = `
        <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
            <img src="/static/images/cross-mark-no-data.png" alt="No data" class="w-32 h-32 mb-4"/>
            <p class="text-center text-gray-600 mt-4">No editor's choice foods at the moment.</p>
        </div>
        `;
        editorChoiceDesc.innerHTML = "Bali offers a wide range of food types, from traditional Balinese cuisine to international dishes. Here are some of the halal editor's choice foods in Bali.";
    } else {
        if (foodType === 'all') {
            editorChoiceDesc.innerHTML = "Bali offers a wide range of food types, from traditional Balinese cuisine to international dishes. Here are some of the halal editor's choice foods in Bali.";
        } else if (foodType === 'breakfast') {
            editorChoiceDesc.innerHTML = "In Bali, life is and will never be short. In that case, grab a bite of these breakfast foods to start your day.";
        } else if (foodType === 'lunch') {
            editorChoiceDesc.innerHTML = "When the sun is at its peak, it's time to enjoy a hearty lunch. In a humid, sweaty weather of Bali, it's always good to have a good palate. Unfortunately, Bali has abundant choice of especially Halal foods.";
        } else if (foodType === 'dinner') {
            editorChoiceDesc.innerHTML = "When the sun sets, the night is still young. Enjoy a good dinner with your loved ones. Bali has a wide range of halal foods to choose from.";
        } else if (foodType === 'souvenir') {
            editorChoiceDesc.innerHTML = "Don't forget to bring home some souvenirs from Bali. Of course you'll gonna love Bali, so that you have to buy the souvenirs. From traditional to modern ones, Bali has it all.";
        }
        const templateResponse = await fetch(`/editors-choice/show/${foodType}/`);
        let templateString = await templateResponse.text();
        templateString = templateString.replace("Last Week", data[0].fields.week);
        editorChoiceList.innerHTML += '<ul role="list" class="divide-y divide-gray-100 hover:fly-out">';

        for (const item of data) {
            const foodItems = await fetchFoodItemsRec(item.fields.food_items);
            // for (const recItems of foodRecItems) {
            //     const foodItems = await fetchFoodItems(recItems.fields.food_item);
                foodItems.forEach(foodItem => {
                    const foodItemUrl = `/editors-choice/food-item/?food_item=${encodeURIComponent(foodItem.fields.name)}&food_id=${foodItem.pk}`;
                    let itemHtml = templateString
                        .replace("#link", foodItemUrl)
                        .replace("Name", DOMPurify.sanitize(foodItem.fields.name))
                        .replace("Description", (DOMPurify.sanitize(foodItem.fields.description.slice(0, 50)) + (foodItem.fields.description.length > 50 ? '...' : '')))
                        .replace("Food Type", DOMPurify.sanitize(foodItem.fields.food_type))
                        .replace("Last Week", DOMPurify.sanitize(item.fields.week));
                    editorChoiceList.innerHTML += itemHtml;
                });
            }
        // }
        editorChoiceList.innerHTML += '</ul>';
    }
}

// Fetch the food recommendation items based on the food item IDs
async function fetchFoodItemsRec(foodItemIds) {
    const foodItems = [];
    for (const foodItemId of foodItemIds) {
        const foodRecommendationResponse = await fetch(`/editors-choice/json/food-rec/${foodItemId}`);
        const foodRecommendationData = await foodRecommendationResponse.json();
        const foodItemResponse = await fetch(`/editors-choice/json/food/${foodRecommendationData[0].fields.food_item}`);
        const foodItemData = await foodItemResponse.json();
        foodItems.push(foodItemData[0]);
    }
    return foodItems;
}

// Fetch the food items based on the food item IDs
async function fetchFoodItems(foodItemId) {
    const response = await fetch(`/editors-choice/json/food/${foodItemId}`);
    const data = await response.json();
    return data;
}

/**
 * Event-listeners methods go here
 */
// Event listener for the header's food type categories links
document.addEventListener('DOMContentLoaded', function() {
    const anchors = document.querySelectorAll('a[id$="ID"]');
    anchors.forEach(anchor => {
      anchor.addEventListener('click', function(event) {
        event.preventDefault();
        const foodType = this.id.replace('ID', '').toLowerCase();
        fetchFoodData(foodType);
      });
    });
});

// Event listener for choosing the food type
async function fetchFoodData(foodType) {
    try {
        let response;
        if (foodType === 'all') {
            response = await fetch('/editors-choice/json/editor-choice/');
        } else {
            response = await fetch(`/editors-choice/json/editor-choice/${foodType}/`);
        }
        const data = await response.json();
        fetchFoodFinisher(data, foodType);
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('editorChoiceList').innerHTML = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <img src="/static/images/cross-mark-no-data.png" alt="No data" class="w-32 h-32 mb-4"/>
                <p class="text-center text-gray-600 mt-4">Data are not inputted yet or failed to connect.</p>
            </div>
        `;
    }
}

// Event listener for the food item page
document.addEventListener('DOMContentLoaded', function() {   
    // Call the updateDescription function
    updateDescriptionForFoodRec();
});

// Function to get query parameters
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        food_item: params.get('food_item'),
        food_id: params.get('food_id')
    };
}

// Function to fetch food item data
async function fetchFoodItemDataHelper(food_item, food_id) {
    try {
        const response = await fetch(`/editors-choice/json/food/${food_id}`);
        const data = await response.json();
        return data[0].fields;
    } catch (error) {
        console.error('Error fetching food item data:', error);
        return null;
    }
}

// Function to fetch rating data from full json database
async function fetchRatingDataHelper(food_item, food_id) {
    const response = await fetch(`/editors-choice/json/food-rec/`);
    const data = await response.json();
    const ratingData = data.find(item => item.fields.food_item === food_id);
    return ratingData;
}

// Function to update the description paragraph
async function updateDescriptionForFoodRec() {
    const { food_item, food_id } = getQueryParams();
    if (food_item && food_id) {
        const item = await fetchFoodItemDataHelper(food_item, food_id);
        if (item) {
            document.getElementById('descParagraph').innerHTML = DOMPurify.sanitize(item.description);
            document.getElementById('productName').innerHTML = DOMPurify.sanitize(item.name);
            const formattedPrice = Number(item.price).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            document.getElementById('productPrice').innerHTML = "Rp" + DOMPurify.sanitize(formattedPrice);
            document.getElementById('highlightProduct').innerHTML = DOMPurify.sanitize(item.name) + " is best eaten at:";
            document.getElementById('bestEatenHighlighted').innerHTML = DOMPurify.sanitize(item.food_type.charAt(0).toUpperCase() + item.food_type.slice(1));
        }
        const ratingData = await fetchRatingDataHelper(food_item, food_id);
        if (ratingData) {
            document.getElementById('anchorToFood').innerHTML = DOMPurify.sanitize(ratingData.fields.rating) + " out of 5 (verified by admin: " + ratingData.fields.author + ")";
        }
    }
}

function showModal() {
    const modal = document.getElementById('crudModal');
    const modalContent = document.getElementById('crudModalContent');

    modal.classList.remove('hidden');
    modal.removeAttribute('aria-hidden');
    modalContent.classList.remove('opacity-0', 'scale-95');
    modalContent.classList.add('opacity-100', 'scale-100');

    setTimeout(() => {
        modalContent.classList.remove('opacity-0', 'scale-95');
        modalContent.classList.add('opacity-100', 'scale-100');
    }, 50);
}

function hideModal() {
    const modal = document.getElementById('crudModal');
    const modalContent = document.getElementById('crudModalContent');

    modalContent.classList.remove('opacity-100', 'scale-100');
    modalContent.classList.add('opacity-0', 'scale-95');

    setTimeout(() => {
        modal.classList.add('hidden');
        modal.setAttribute('aria-hidden', 'true');
    }, 150);
}

// Function to submit the edited rating via AJAX
async function submitEditRating() {
    // Extract food_id from URL
    const urlParams = new URLSearchParams(window.location.search);
    const foodItemId = urlParams.get('food_id');

    // Fetch from the full FoodRecommendation JSON database
    const responseFR = await fetch(`/editors-choice/json/food-rec/`);
    const dataFR = await responseFR.json();

    // Find the food item in the FoodRecommendation database
    const foodItem = dataFR.find(item => item.fields.food_item === foodItemId);
    const foodRecommendationId = foodItem.pk;

    // const rating = parseFloat(document.getElementById('rating').value); // Ensure rating is a float
    const formElement = document.getElementById('editRatingForm');

    const response = await fetch(`/editors-choice/edit-food/?food_recommendation_id=${foodRecommendationId}`, {
        method: 'POST',
        body: new FormData(formElement)
    }).then(response => updateDescriptionForFoodRec());
    formElement.reset();
    document.querySelector('[data-modal-toggle="crudModal"]').click();

    if (response.ok) {
        const data = await response.json();
        alert(data.message);
        document.getElementById('crudModal').classList.add('hidden');
    } else {
        alert('Failed to update rating.');
    }
}

document.getElementById("cancelButton").addEventListener("click", hideModal);
document.getElementById("closeModalBtn").addEventListener("click", hideModal);
document.getElementById("submitEditRating").addEventListener("click", hideModal);
document.getElementById('submitEditRating').addEventListener("click", (event) => {
    event.preventDefault();
    submitEditRating();
});