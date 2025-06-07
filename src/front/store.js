export const initialStore=()=>{
  return{
    message: null,
    token: null,
    
  }
}

export default function storeReducer(store, action = {}) {
  switch(action.type){
    case 'set_hello':
      return {
        ...store,
        message: action.payload
      };
      
    case 'add_task':

      const { id,  color } = action.payload

      return {
        ...store,
        todos: store.todos.map((todo) => (todo.id === id ? { ...todo, background: color } : todo))
      };

      case 'fetchedToken':
        break;
        
    default:
      throw Error('Unknown action.');
  }    
}
