import React, {useState} from 'react'
function Header(){
    return (
        <div>
            <h1 className = "welcome-message">
            <div href="{% url 'home' %}">
                Welcome to user.username BlogSpace!
            </div>
            </h1>
            <div className="header">
                <div className="left-header">
                    <button className="create-button">
                        <div>Create new Blog</div>
                    </button>
                </div>
                <div className="middle-header">
                    <form>
                        <div className="search-bar">
                            <input id="search" type="search" name="q" placeholder="Search"/>
                            <input className = "search-button" type="submit" value="submit"/>
                        </div>
                    </form>
                    <p>message </p>
                </div>
                <div className="right-header">
                    <button className="notification-button">
                        <div>
                        Notifications
                        <p className="num-requests"> num_requests </p>
                        </div>
                    </button>
                    <button className="logout-button">
                        <div>Log out</div>
                    </button>
                </div>
            </div>
        </div>
    )
}

export default Header;
