import Utility from '../welcome_page/utility'
import './css/blog_post.css'
export default function Post(props){
    console.log('props for post', props)

    const handleClick = (newMain) =>{
        Utility.changeMain(props.display.setDisplay, newMain);
        props.display.setDisplay((oldValue) =>{
            return {
                ...oldValue,
                'postId':props.id,

            }
        })
    }

    const handleMouseEnter = event =>{
        const name  = event.target.dataset['name']
        const username = props.display.memberData.user.username
        if(name === username){
            event.target.children[1].className = 'post-button-container'

        }else{
            console.log('do not display')
        }
    }

    const handleMouseLeave = event =>{
        console.log('leave', event)
        if(event.target.children.length > 0){
            event.target.children[1].className = 'post-hide-container'
        }
    }


    return(
        <div data-name={props.username} className="post-message" onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <div className='post-container'>
                <p > {props.username} </p><br/>
                <p> {props.txt_message} </p><br/>
                <p> {props.date} </p>
            </div>
            <div className='post-hide-container'>
                <div  onClick={() => handleClick('remove')}>remove</div>
                <div onClick={() => handleClick('update')}>update</div>
            </div>
        </div>
    )
}