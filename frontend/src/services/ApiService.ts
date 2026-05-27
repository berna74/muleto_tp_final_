import {instance as axios} from '../plugins/axios';

class ApiService {
  static async getAll(url: string) {
    const response = await ApiService.get(url);
    return response.data;
  }

  static async getOne(url: string, id: number) {
    const response = await ApiService.get(`${url}/${id}`);
    return response.data;
  }

  static async create(url: string, data: object) {
    const response = await ApiService.post(url, data);
    return response.data;
  }

  static async update(url: string, id: number, data: object) {
    const response = await ApiService.put(`${url}/${id}`, data);
    return response.data;
  }

  static async destroy(url: string, id: number) {
    const response = await ApiService.delete(`${url}/${id}`);
    return response.data;
  }

  static async get(url: string) {
    try {
      const response = await axios.get(url);
      return response;
    } catch (error) {
      console.error('Error en GET:', error);
      throw error;
    }
  }

  static async post(url: string, data: object) {
    try {
      const response = await axios.post(url, data);
      return response;
    } catch (error) {
      console.error('Error en POST:', error);
      throw error;
    }
  }

  static async put(url: string, data: object) {
    try {
      const response = await axios.put(url, data);
      return response;
    } catch (error) {
      console.error('Error en PUT:', error);
      throw error;
    }
  }

  static async delete(url: string) {
    try {
      const response = await axios.delete(url);
      return response;
    } catch (error) {
      console.error('Error en DELETE:', error);
      throw error;
    }
  }
}

export default ApiService;