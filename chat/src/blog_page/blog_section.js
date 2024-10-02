import React, {useState} from 'react'
import Blog from './blog'
function BlogSection(props){
    let data = props.display.memberData
    const displayBlogs = data[props.type].map((blog) =>{
        if (props.type === 'recents'){
            blog = blog['recent_blog']
        }
        return <Blog {...blog} key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)}/>
    })
    console.log(displayBlogs)
    return (
        <div>
            {displayBlogs}
        </div>
    )   
}
export default BlogSection