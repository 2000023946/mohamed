

const Utility = {
    handleClick: (props, display) => handleClick(props, display),
    updateData: (e, setData) => updateData(e, setData),
}


function handleClick(props, display){
  props.setter(display)
  window.history.pushState({'name':display}, '', display)
  localStorage.setItem('page', display)
}

function updateData(e, setData){
  setData((prevValue) =>{
      return {
          ...prevValue,
          [e.target.name]:e.target.value
      }
  })
}

export default Utility;