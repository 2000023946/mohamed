import React, {useState} from 'react'
import Blog from './blog'
import Utility from '../welcome_page/utility'
function BlogSection(props){
    let data = props.display.memberData

    const handleClick = (props, blog) =>{
        Utility.isAllowed(props, blog)
    }

    const displayBlogs = data[props.type].map((blog) =>{
        if (props.type === 'recents'){
            blog = blog['recent_blog']
        }
        return <Blog handleClick={() =>handleClick(props, blog)}  {...blog} key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)}/>
    })
    return (
        <div>
            
            {displayBlogs}
        </div>
    )   
}
export default BlogSection;