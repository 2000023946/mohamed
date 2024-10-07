function Blog(props){


    return(
        <div onClick={props.handleClick}>
            <div className="blog-contents">
                <div>
                    <div className ="blog-container">
                        <div className="blog-title">
                            <h3 > {props.title} </h3>
                        </div>
                        <div className="blog-description">
                            <p className="description"> {props.description} </p>
                        </div>
                        <div className="bottom-blog-section">
                            <div className="creators-users">
                                <p className="creator">Creator : {props.created_user.username}</p>
                                <p className="users"> Chatters :  {props.number_users} </p>
                            </div>
                            <div className="date-section">
                                <p className="date">  {props.date} </p>
                            </div>
                            <div className="status">
                                <p>{props.state}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Blog;