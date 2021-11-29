import 'main/index.scss';


export function vt() {
    return ['span', `temperature: ${r.get('remote', 'temperature')}`];
}
