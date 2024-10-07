import Utility from '../welcome_page/utility'

import React, {useState} from 'react'

export default function Request(props){

    const [selectedValue, setSelectedValue] = useState(true)

    const handleChange = event =>{
        setSelectedValue(event.target.value)
    }


    const submitData = event =>{
        event.preventDefault();
        console.log(selectedValue)
        fetch('http://localhost:8000/api/request/',{
            method:'PUT',
            headers:{
                'Content-type':'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`
            },
            body:JSON.stringify({
                'id': props.id,
                'is_accpeted':selectedValue
            })
        }).then(resp => resp.json())
        .then(data =>{
            console.log(data)
            props.display.setDisplay((oldValue) =>{
                return {
                    ...oldValue,
                    'memberData':{
                        ...props.display.memberData,
                        'request': props.display.memberData.request.filter(requestData => requestData.id !== data.id)
                    }
                }
            })
            localStorage.setItem('user', props.display.memberData)
            console.log(props)
        })
    }

    return (
        <div className ="notify-msg">
            <p>From :  {props.user_from.username} </p><br/>
            <p> Blog: {props.blog.title} </p>
            <form onSubmit={submitData}>
                <select value={selectedValue} onChange={handleChange} name="notify-select" id="">
                    <option value={true}>Accept</option>
                    <option value={false}>Decline</option>
                </select>
                <input type="submit" value="Submit"/>
            </form>
        </div>
    )
}