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
                    <a href="#" class="block px-4 py-2 text-sm text-gray-700" role="menuitem" tabindex="-1" id="user-menu-item-1">Settings</a>
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
    // Update the header links when the page is changed
    async function superuserFeatures() {
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
    superuserFeatures();

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
                <img src="/static/image/cross-mark-no-data.png" alt="No data" class="w-32 h-32 mb-4"/>
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
            <img src="/static/image/cross-mark-no-data.png" alt="No data" class="w-32 h-32 mb-4"/>
            <p class="text-center text-gray-600 mt-4">No editor's choice foods at the moment.</p>
        </div>
        `;
        editorChoiceDesc.innerHTML = "Bali offers a wide range of food types, from traditional Balinese cuisine to international dishes. Here are some of the halal editor's choice foods in Bali.";
    } else {
        const templateResponse = await fetch(`/editors-choice/show/${foodType}`);
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
                        .replace("Description", DOMPurify.sanitize(foodItem.fields.description))
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
    const response = await fetch(`/editors-choice/json/food-item/${foodItemId}`);
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
            response = await fetch(`/editors-choice/json/editor-choice/${foodType}`);
        }
        const data = await response.json();
        fetchFoodFinisher(data, foodType);
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('editorChoiceList').innerHTML = `
            <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                <img src="/static/image/cross-mark-no-data.png" alt="No data" class="w-32 h-32 mb-4"/>
                <p class="text-center text-gray-600 mt-4">Data are not inputted yet or failed to connect.</p>
            </div>
        `;
    }
}