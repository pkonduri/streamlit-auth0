import { Streamlit } from "streamlit-component-lib"
import createAuth0Client from '@auth0/auth0-spa-js';
import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"
import "./style.css"

const div = document.body.appendChild(document.createElement("div"))
const button = div.appendChild(document.createElement("button"))
button.className = "log"
button.textContent = "Login"
let isLoggedIn = false; // Track login status
let desiredButtonText = "Login"; // Default text


// set flex collumn so the error message appears under the button
div.style = "display: flex; flex-direction: column; color: rgb(104, 85, 224); font-weight: 600; margin: 0; padding: 10px"
const errorNode = div.appendChild(document.createTextNode(""))

// Global vars
let client_id
let domain
let auth0

function updateButtonText() {
  if (isLoggedIn) {
    button.textContent = "Logout"; // Text to display when logged in
  } else {
    button.textContent = desiredButtonText; // Text from Python or default
  }
}

const logout = async () => {
  auth0.logout({returnTo: getOriginUrl()})
  Streamlit.setComponentValue(false)
  // button.textContent = "Login"
  // Update login status and button text
  isLoggedIn = false; // Update login status
  updateButtonText(); // Update button text
  button.removeEventListener('click', logout)
  button.addEventListener('click', login)
}

const login = async () => {
  button.textContent = 'working...'
  console.log('Callback urls set to: ', getOriginUrl())
  auth0 = await createAuth0Client({
      domain: domain,
      client_id: client_id,
      redirect_uri: getOriginUrl(),
      audience:`https://${domain}/api/v2/`,
      useRefreshTokens: true,
      cacheLocation: "localstorage",
    });

    // Remove the event listener for login before adding a new one for logout
    button.removeEventListener('click', login);

    try{
      await auth0.loginWithPopup();
      errorNode.textContent = ''
    }
    catch(err){
      console.log(err)
      errorNode.textContent = `Popup blocked, please try again or enable popups` + String.fromCharCode(160)
      return
    }
    const user = await auth0.getUser();
    console.log(user)
    console.log({
      // return getAccessTokenWithPopup({
        audience:`https://${domain}/api/v2/`,
        scope: "read:current_user",
      })
    let token = false
    
    try{
    token = await auth0.getTokenSilently({
        // return getAccessTokenWithPopup({
          audience:`https://${domain}/api/v2/`,
          // scope: "read:current_user",
        });
      }
      catch(error){
        if (error.error === 'consent_required' || error.error === 'login_required'){
          console.log('asking user for permission to their profile')
           token = await auth0.getTokenWithPopup({
              audience:`https://${domain}/api/v2/`,
              scope: "read:current_user",
            });
            console.log(token)
        }
        else{console.log(error)}
      }

    let userCopy = JSON.parse(JSON.stringify(user));
    userCopy.token = token
    console.log(userCopy);
    Streamlit.setComponentValue(userCopy)
    // button.textContent = "Logout"

    // Update login status and button text
    isLoggedIn = true; // Update login status
    updateButtonText(); // Update button text

    button.removeEventListener('click', login)
    button.addEventListener('click', logout)
}

// Make sure to initialize the button's event listener with the login function
button.addEventListener('click', login);
//button.onclick = login

function onRender(event) {
  const data = event.detail;
  
  client_id = data.args["client_id"];
  domain = data.args["domain"];
  
  // Update desiredButtonText but don't directly change the button text here
  desiredButtonText = data.args["button_text"] || "Login";

  // Let updateButtonText handle setting the button text
  updateButtonText();

  Streamlit.setFrameHeight();
}


Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()

const getOriginUrl = () => {
  // Detect if you're inside an iframe
  if (window.parent !== window) {
    const currentIframeHref = new URL(document.location.href)
    const urlOrigin = currentIframeHref.origin
    const urlFilePath = decodeURIComponent(currentIframeHref.pathname)
    // Take referrer as origin
    return urlOrigin + urlFilePath
  } else {
    return window.location.origin
  }
}

// Initial call to set the correct button text based on the current state
updateButtonText();