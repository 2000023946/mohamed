import React, {useState, useEffect} from 'react';
import './css/header.css'
import BlogPage from './blog_page'
import Header from './header'
import BlogPost from './blog-post'
import CreateBlog from './create_blog'
import Notification from './notification';
import SearchResult from './serach_result';

function BlogHome(props){

    const [postData, setPostData] = useState({})

    return(
        <div>  
            {   props.display.main === 'home' && 
                <div>
                    <Header username={props.display.memberData.user.username} {...props}/>
                    <BlogPage post={{'postData':postData, 'setPostData':setPostData}} {...props}/>
                </div>
            }
            {
                props.display.main === 'search' && 
                <div>
                    <Header username={props.display.memberData.user.username} {...props}/>
                    <SearchResult {...{...props, 'post': {'postData':postData, 'setPostData':setPostData}}}/>
                </div>            
            }
            {props.display.main === 'notification' && <Notification {...props} />}
            {props.display.main === 'create_blog' && <CreateBlog {...{...props, 'post': {'postData':postData, 'setPostData':setPostData}}} />}
            {props.display.main === 'post' && <BlogPost {...{...props, 'post': {'postData':postData, 'setPostData':setPostData}}} /> }
        </div>
    )
}

export default BlogHome;