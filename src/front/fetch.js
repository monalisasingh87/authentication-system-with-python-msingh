export const login =async(email, password, dispatch) =>{
    const options ={
        method : "POST",
        mode: 'cors',
        headers: {
            'Content- Type': 'application/json'
        }
        body : JSON.stringify({
            email: email,
            password: password
        })
    }

   const response = await fetch('https://silver-train-jj446v796p9vfp5wq-3001.app.github.dev/api/token', options)

   try{
    if (!response.ok) {
        throw new Error(response.status);
    }

    const data = await response.json();
    console.log(data);
    dispatch({
        type: 'fetchedToken',
        payload: data
    })
   }
   catch (error) {
    console.error('Error fetching token.', error)
   }

}
