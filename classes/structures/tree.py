from fixtures.block_fixture import wooden_log, leave


class Tree():
    trunk_rows = 3
    leave_5_rows = 2
    leave_3_rows = 2

    def generate(self, x, y, blocks):
        # trunk
        for wood_y in range(self.trunk_rows):
            blocks[(x, y - wood_y, 1)] = wooden_log.id

        # 5 width leave rows
        for leave_5_y in range(self.leave_5_rows):
            for leave_5_x in range(-2, 3):
                blocks[(x + leave_5_x, y - self.trunk_rows - leave_5_y, 1)] = leave.id

        # 3 width leave rows
        for leave_3_y in range(self.leave_3_rows):
            for leave_3_x in range(-1, 2):
                blocks[(x + leave_3_x, y - self.trunk_rows - self.leave_5_rows - leave_3_y, 1)] = leave.id