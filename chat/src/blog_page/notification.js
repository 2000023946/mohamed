import './css/notify.css'
import Request from './request'
import Utility from '../welcome_page/utility'
import {useEffect, useState} from 'react'
export default function Notification(props){


    //const requestList = []

    //const [updatedRequestList, setUpdatedRequestList] = useState([])

    const updatedRequestList = []

    props.display.memberData.request.forEach(element => {
        let shouldAdd = true
        updatedRequestList.forEach(item =>{
            if (item.id === element.id){
                shouldAdd = false
            }
        })
        if(shouldAdd){
            updatedRequestList.push(element)
        }
    });
    console.log('request list', updatedRequestList)
    useEffect(()=>{
        props.display.setDisplay((oldValue) =>{
            return{
                ...oldValue,
                'memberData':{
                ...props.display.memberData,
                'request': updatedRequestList
                }
            }
        })
    }, [])
    console.log('new props', props)

    const requestList = props.display.memberData.request.map(request =>{
        console.log(request)
        const requestInfo = {
            'username':request.user_from.username,
            'blog':request.blog.title,
            'id':request.id,
        }
        console.log(requestInfo)
        return <Request  {...props} {...requestInfo} key={Math.random(1)*Math.random(1)*Math.random(1)*Math.random(1)}/>
    })


    return (
        <div className='notify'>
            <div className="notify-title">
                <button className="notify-button">
                    <div onClick={() =>Utility.changePage(props, 'home')}>go back</div>
                </button>
                <h1>Requests</h1>
            </div>
            {requestList}
        </div>
    )
}