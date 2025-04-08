import { get, post } from '/@/utils/http/axios';
enum URL {
    list = '/myapp/admin/zxsubmit/suanfa',
}
const listApi = async (params?: any) => get<any>({ url: URL.list, timeout: 90000,params: params || {} });
export { listApi};