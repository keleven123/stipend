import { get, post } from '/@/utils/http/axios';

enum URL {
    create = '/myapp/admin/zxsubmit/create',
    detail = '/myapp/admin/zxsubmit/application_detail',
    delete = '/myapp/admin/zxsubmit/delete',
    list = '/myapp/admin/zxsubmit/list',
    update = '/myapp/admin/zxsubmit/update',
}

const createApi = async (data: any) =>
    post<any>({ url: URL.create, params: {}, data: data, timeout:20000, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
const detailApi = async (params: any) => get<any>({ url: URL.detail, params: params, headers: {} });
const deleteApi = async (params: any) => post<any>({ url: URL.delete, params: params, headers: {} });
const listApi = async (params: any) =>
    get<any>({url: URL.list, params: params, data: {}, headers: {}});
const updateApi = async (params: any, data: any) =>
    post<any>({ url: URL.update, params: params, data: data, headers: { 'Content-Type': 'multipart/form-data;charset=utf-8' } });
export {  createApi,  deleteApi, detailApi ,listApi,updateApi};