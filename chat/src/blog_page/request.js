import Utility from '../welcome_page/utility'

import React, {useState, useEffect} from 'react'

export default function Request(props){

    const [selectedValue, setSelectedValue] = useState(true)

    const handleChange = event =>{
        setSelectedValue(event.target.value)
    }

    console.log(props)

    const submitData = event =>{
        event.preventDefault();
        console.log(selectedValue)
        fetch(`http://localhost:8000/api/request/${props.id}`,{
            method:'PUT',
            headers:{
                'Content-type':'application/json',
                'Authorization': `Token ${localStorage.getItem('token')}`
            },
            body:JSON.stringify({
                'id': props.id,
                'is_accepted':selectedValue
            })
        }).then(resp => resp.json())
        .then(data =>{
            console.log(data)
            const newRequestList = []
             props.display.memberData.request.forEach(element => {
                if (element.id !== data.id){
                    newRequestList.push(element)
                }
            });

            props.display.setDisplay((oldValue) =>{
                return {
                    ...oldValue,
                    'memberData':{
                        ...props.display.memberData,
                        'request': newRequestList
                    }
                }
            })
            sendMessage({'data':data, 'type':'update request', 'user':data['user_from']['username']})
            localStorage.setItem('user', JSON.stringify(props.display.memberData))
            console.log(props.display.memberData)
        })
    }

    const [socket, setSocket] = useState(null)

    useEffect(() =>{
        const socket = new WebSocket(`ws://localhost:8000/ws/request/${props.display.memberData.user.username}/`)
        setSocket(socket)

        socket.onopen = event =>{
        console.log(event)
        }
        socket.onmessage = event =>{
            console.log('new event', event)
            console.log(event.data)
            const data = JSON.parse(event.data)
            console.log(data)
            if(data['type'] === 'update request'){
                console.log('your reqeust got updated')
                console.log(data)
            }
        }
        socket.onclose = event =>{
        console.log(event)
        }

    }, [])

    const sendMessage = (message) =>{
        socket.send(JSON.stringify(message))
    }


    const requestInfo = props.data

    return (
        <div className ="notify-msg">
            <p>From : {props.username} </p><br/>
            <p> Blog: {props.blog} </p>
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