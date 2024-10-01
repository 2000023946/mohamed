import React, {useState} from 'react'

function BlogSection(props){
    return (
        <div>
            <h1>{props.name}</h1>
            <div className="blog-contents">
                <div>
                    <div className ="blog-container">
                        <div className="blog-title">
                            <h3 > blog.title </h3>
                        </div>
                        <div className="blog-description">
                            <p className="description"> blog.description </p>
                        </div>
                        <div className="bottom-blog-section">
                            <div className="creators-users">
                                <p className="creator">Creator : blog.created_user.username</p>
                                <p className="users"> Chatters :  blog.number_users </p>
                            </div>
                            <div className="date-section">
                                <p className="date">  blog.date </p>
                            </div>
                            <div className="status">
                                <p>Public</p>
                                <p>Private</p>
                            </div>
                        </div>
                        <p>no reccomendations </p>
                    </div>
                </div>
            </div>
        </div>
    )   
}
export default BlogSection