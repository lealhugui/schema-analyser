import $ from 'jquery'; 

/*
	General constans and utils of the client
*/

/* Backend API URL */
export const API_URL = window.location.hostname+":8000";

export const removeLogoAnimation = () => {
	const logo = $("#app-logo");
	setTimeout(() => logo.removeClass("animated"), 1000);
}

export const addLogoAnimation = () => {
	const logo = $("#app-logo");
	logo.addClass("animated");
}

export const handleErr = (err) => {
	console.error(err);
	if ("err" in err) {
		alert(err.err);
	} else {
		alert(err);
	}
}