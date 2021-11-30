import asyncio
import hat.aio
import hat.event.common
import hat.gateway.common
from hat.drivers import modbus, tcp


json_schema_id = None
json_schema_repo = None
device_type = 'modbus'


async def create(conf, event_client, event_type_prefix):
    device = ModbusDevice()

    device._async_group = hat.aio.Group()
    device._event_client = event_client
    device._event_type_prefix = event_type_prefix
    device._task = asyncio.create_task(device._main_loop())

    return device


class ModbusDevice(hat.gateway.common.Device):

    @property
    def async_group(self):
        return self._async_group

    async def _main_loop(self):
        modbus_type = modbus.ModbusType.TCP
        address = tcp.Address('161.53.17.239', 8502)
        master = await modbus.create_tcp_master(modbus_type, address)
        while True:
            data = await master.read(
                device_id=1,
                data_type=modbus.DataType.HOLDING_REGISTER,
                start_address=4003, quantity=1)
            self._event_client.register([
                hat.event.common.RegisterEvent(
                    event_type=(*self._event_type_prefix,
                                'gateway', '4003'),
                    source_timestamp=None,
                    payload=hat.event.common.EventPayload(
                        type=hat.event.common.EventPayloadType.JSON,
                        data=data[0]))])
