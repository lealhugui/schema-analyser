import $ from 'jquery'; 

/*
	General constans and utils of the client
*/

/* Backend API URL */
export const API_URL = window.location.hostname+":8000";

export function removeLogoAnimation() {
	const logo = $("#app-logo");
	console.log(logo);
	setTimeout(() => logo.removeClass("animated"), 1000);	
}

export function addLogoAnimation() {
	const logo = $("#app-logo");
	console.log(logo);
	logo.addClass("animated");
}