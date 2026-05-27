import {instance as axios} from '../plugins/axios';

class ServicioApi {
  static async obtenerTodo(url: string) {
    const response = await ServicioApi.obtener(url);
    return response.data;
  }

  static async obtenerUno(url: string, id: number) {
    const response = await ServicioApi.obtener(`${url}/${id}`);
    return response.data;
  }

  static async crear(url: string, data: object) {
    const response = await ServicioApi.enviar(url, data);
    return response.data;
  }

  static async actualizar(url: string, id: number, data: object) {
    const response = await ServicioApi.modificar(`${url}/${id}`, data);
    return response.data;
  }

  static async eliminarUno(url: string, id: number) {
    const response = await ServicioApi.eliminar(`${url}/${id}`);
    return response.data;
  }

  static async obtener(url: string) {
    try {
      const response = await axios.get(url);
      return response;
    } catch (error) {
      console.error('Che, falló la consulta GET:', error);
      throw error;
    }
  }

  static async enviar(url: string, data: object) {
    try {
      const response = await axios.post(url, data);
      return response;
    } catch (error) {
      console.error('Che, falló el envío POST:', error);
      throw error;
    }
  }

  static async modificar(url: string, data: object) {
    try {
      const response = await axios.put(url, data);
      return response;
    } catch (error) {
      console.error('Che, falló la actualización PUT:', error);
      throw error;
    }
  }

  static async eliminar(url: string) {
    try {
      const response = await axios.delete(url);
      return response;
    } catch (error) {
      console.error('Che, falló la baja DELETE:', error);
      throw error;
    }
  }

}

export default ServicioApi;